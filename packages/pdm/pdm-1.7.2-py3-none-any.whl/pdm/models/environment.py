from __future__ import annotations

import collections
import os
import shlex
import shutil
import subprocess
import sys
import sysconfig
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Any, Generator, Iterator

from pip._vendor import packaging, pkg_resources

from pdm import termui
from pdm.exceptions import BuildError
from pdm.models import pip_shims
from pdm.models.auth import make_basic_auth
from pdm.models.in_process import (
    get_pep508_environment,
    get_python_abi_tag,
    get_sys_config_paths,
)
from pdm.models.pip_shims import misc, patch_bin_prefix, req_uninstall
from pdm.utils import cached_property, expand_env_vars_in_auth, get_finder, temp_environ

if TYPE_CHECKING:
    from pdm._types import Source
    from pdm.models.python import PythonInfo
    from pdm.project import Project


def _get_shebang_path(executable: str, is_launcher: bool) -> bytes:
    """Get the interpreter path in the shebang line

    The launcher can just use the command as-is.
    Otherwise if the path contains whitespace or is too long, both distlib
    and installer use a clever hack to make the shebang after ``/bin/sh``,
    where the interpreter path is quoted.
    """
    if is_launcher or " " not in executable and (len(executable) + 3) <= 127:
        return executable.encode("utf-8")
    return shlex.quote(executable).encode("utf-8")


class WorkingSet(collections.abc.Mapping):
    """A dict-like class that holds all installed packages in the lib directory."""

    def __init__(
        self,
        paths: list[str] | None = None,
        python: str = pkg_resources.PY_MAJOR,
    ):
        self.env = pkg_resources.Environment(paths, python=python)
        self.pkg_ws = pkg_resources.WorkingSet(paths)
        self.__add_editable_dists()

    def __getitem__(self, key: str) -> pkg_resources.Distribution:
        rv = self.env[key]
        if rv:
            return rv[0]
        else:
            raise KeyError(key)

    def __len__(self) -> int:
        return len(self.env._distmap)

    def __iter__(self) -> Iterator[str]:
        return iter(self.env)

    def __add_editable_dists(self) -> None:
        """Editable distributions are not present in pkg_resources.WorkingSet,
        Get them from self.env
        """
        missing_keys = [key for key in self if key not in self.pkg_ws.by_key]
        for key in missing_keys:
            self.pkg_ws.add(self[key])


class Environment:
    """Environment dependent stuff related to the selected Python interpreter."""

    is_global = False

    def __init__(self, project: Project) -> None:
        """
        :param project: the project instance
        """
        self.python_requires = project.python_requires
        self.project = project
        self.interpreter: PythonInfo = project.python
        self._essential_installed = False
        self.auth = make_basic_auth(
            self.project.sources, self.project.core.ui.verbosity >= termui.DETAIL
        )

    def get_paths(self) -> dict[str, str]:
        """Get paths like ``sysconfig.get_paths()`` for installation."""
        paths = sysconfig.get_paths()
        scripts = "Scripts" if os.name == "nt" else "bin"
        packages_path = self.packages_path
        paths["platlib"] = paths["purelib"] = (packages_path / "lib").as_posix()
        paths["scripts"] = (packages_path / scripts).as_posix()
        paths["data"] = paths["prefix"] = packages_path.as_posix()
        paths["include"] = paths["platinclude"] = paths["headers"] = (
            packages_path / "include"
        ).as_posix()
        return paths

    @contextmanager
    def activate(self) -> Iterator:
        """Activate the environment. Manipulate the ``PYTHONPATH`` and patches ``pip``
        to be aware of local packages. This method acts like a context manager.

        :param site_packages: whether to inject base site-packages into the sub env.
        """
        paths = self.get_paths()
        with temp_environ():
            working_set = self.get_working_set()
            _old_ws = pkg_resources.working_set
            pkg_resources.working_set = working_set.pkg_ws  # type: ignore
            # HACK: Replace the is_local with environment version so that packages can
            # be removed correctly.
            _old_sitepackages = misc.site_packages
            misc.site_packages = paths["purelib"]
            _is_local = misc.is_local
            misc.is_local = req_uninstall.is_local = self.is_local
            _evaluate_marker = pkg_resources.evaluate_marker
            pkg_resources.evaluate_marker = self.evaluate_marker
            sys._original_executable = sys.executable  # type: ignore
            sys.executable = self.interpreter.executable
            with patch_bin_prefix(paths["scripts"]):
                yield
            sys.executable = sys._original_executable  # type: ignore
            del sys._original_executable  # type: ignore
            pkg_resources.evaluate_marker = _evaluate_marker
            misc.is_local = req_uninstall.is_local = _is_local
            misc.site_packages = _old_sitepackages
            pkg_resources.working_set = _old_ws

    def is_local(self, path: str) -> bool:
        """PEP 582 version of ``is_local()`` function."""
        return misc.normalize_path(path).startswith(
            misc.normalize_path(self.packages_path.as_posix())
        )

    def evaluate_marker(self, text: str, extra: Any = None) -> bool:
        marker = packaging.markers.Marker(text)
        return marker.evaluate(self.marker_environment)

    @cached_property
    def packages_path(self) -> Path:
        """The local packages path."""
        pypackages = (
            self.project.root  # type: ignore
            / "__pypackages__"
            / self.interpreter.identifier
        )
        if not pypackages.exists() and "-32" in pypackages.name:
            compatible_packages = pypackages.with_name(pypackages.name[:-3])
            if compatible_packages.exists():
                pypackages = compatible_packages
        scripts = "Scripts" if os.name == "nt" else "bin"
        if not pypackages.parent.exists():
            pypackages.parent.mkdir(parents=True)
            pypackages.parent.joinpath(".gitignore").write_text("*\n!.gitignore\n")
        for subdir in [scripts, "include", "lib"]:
            pypackages.joinpath(subdir).mkdir(exist_ok=True, parents=True)
        return pypackages

    @contextmanager
    def get_finder(
        self,
        sources: list[Source] | None = None,
        ignore_requires_python: bool = False,
    ) -> Generator[pip_shims.PackageFinder, None, None]:
        """Return the package finder of given index sources.

        :param sources: a list of sources the finder should search in.
        :param ignore_requires_python: whether to ignore the python version constraint.
        """
        if sources is None:
            sources = self.project.sources
        sources = [
            dict(source, url=expand_env_vars_in_auth(source["url"]))  # type: ignore
            for source in sources
        ]

        python_version = self.interpreter.version_tuple
        python_abi_tag = get_python_abi_tag(self.interpreter.executable)
        finder = get_finder(
            sources,
            self.project.cache_dir.as_posix(),
            python_version,
            python_abi_tag,
            ignore_requires_python,
        )
        # Reuse the auth across sessions to avoid prompting repeatly.
        finder.session.auth = self.auth  # type: ignore
        yield finder
        finder.session.close()  # type: ignore

    def get_working_set(self) -> WorkingSet:
        """Get the working set based on local packages directory."""
        paths = self.get_paths()
        return WorkingSet(
            [paths["platlib"], paths["purelib"]],
            python=f"{self.interpreter.major}.{self.interpreter.minor}",
        )

    @cached_property
    def marker_environment(self) -> dict[str, Any]:
        """Get environment for marker evaluation"""
        return get_pep508_environment(self.interpreter.executable)

    def which(self, command: str) -> str | None:
        """Get the full path of the given executable against this environment."""
        if not os.path.isabs(command) and command.startswith("python"):
            python = os.path.splitext(command)[0]
            version = python[6:]
            this_version = self.interpreter.version
            if not version or str(this_version).startswith(version):
                return self.interpreter.executable
        # Fallback to use shutil.which to find the executable
        this_path = self.get_paths()["scripts"]
        python_root = os.path.dirname(self.interpreter.executable)
        new_path = os.pathsep.join([python_root, this_path, os.getenv("PATH", "")])
        return shutil.which(command, path=new_path)

    def update_shebangs(self, old_path: str, new_path: str) -> None:
        """Update the shebang lines"""
        scripts = self.get_paths()["scripts"]
        for child in Path(scripts).iterdir():
            if not child.is_file() or child.suffix not in (".exe", ".py", ""):
                continue
            is_launcher = child.suffix == ".exe"
            old_shebang = _get_shebang_path(old_path, is_launcher)
            new_shebang = _get_shebang_path(new_path, is_launcher)
            child.write_bytes(child.read_bytes().replace(old_shebang, new_shebang, 1))

    def _download_pip_wheel(self, path: str | Path) -> None:
        dirname = Path(tempfile.mkdtemp(prefix="pip-download-"))
        try:
            subprocess.check_call(
                [
                    getattr(sys, "_original_executable", sys.executable),
                    "-m",
                    "pip",
                    "download",
                    "--only-binary=:all:",
                    "-d",
                    str(dirname),
                    "pip<21",  # pip>=21 drops the support of py27
                ],
            )
            wheel_file = next(dirname.glob("pip-*.whl"))
            shutil.move(str(wheel_file), path)
        except subprocess.CalledProcessError:
            raise BuildError("Failed to download pip for the given interpreter")
        finally:
            shutil.rmtree(dirname, ignore_errors=True)

    @cached_property
    def pip_command(self) -> list[str]:
        """Get a pip command for this environment, and download one if not available.
        Return a list of args like ['python', '-m', 'pip']
        """
        from pip import __file__ as pip_location

        python_major = self.interpreter.major
        executable = self.interpreter.executable
        proc = subprocess.run(
            [executable, "-Esm", "pip", "--version"], capture_output=True
        )
        if proc.returncode == 0:
            # The pip has already been installed with the executable, just use it
            return [executable, "-Esm", "pip"]
        if python_major == 3:
            # Use the host pip package.
            return [executable, "-Es", os.path.dirname(pip_location)]
        # For py2, only pip<21 is eligible, download a pip wheel from the Internet.
        pip_wheel = self.project.cache_dir / "pip.whl"
        if not pip_wheel.is_file():
            self._download_pip_wheel(pip_wheel)
        return [executable, str(pip_wheel / "pip")]


class GlobalEnvironment(Environment):
    """Global environment"""

    is_global = True

    def get_paths(self) -> dict[str, str]:
        paths = get_sys_config_paths(self.interpreter.executable)
        paths["prefix"] = paths["data"]
        paths["headers"] = paths["include"]
        return paths

    def is_local(self, path: str) -> bool:
        return misc.normalize_path(path).startswith(
            misc.normalize_path(self.get_paths()["prefix"])
        )

    @property
    def packages_path(self) -> Path | None:  # type: ignore
        return None
