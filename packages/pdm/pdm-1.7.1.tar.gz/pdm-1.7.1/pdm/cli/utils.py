from __future__ import annotations

import argparse
import os
from argparse import Action, _ArgumentGroup
from collections import ChainMap
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Mapping, MutableMapping, cast

import atoml
from packaging.specifiers import SpecifierSet
from pip._vendor.pkg_resources import Distribution
from resolvelib.structs import DirectedGraph

from pdm import termui
from pdm.exceptions import PdmUsageError, ProjectError
from pdm.formats import FORMATS
from pdm.formats.base import make_array, make_inline_table
from pdm.models.environment import WorkingSet
from pdm.models.requirements import Requirement, strip_extras
from pdm.models.specifiers import get_specifier
from pdm.project import Project

if TYPE_CHECKING:
    from resolvelib.resolvers import RequirementInformation, ResolutionImpossible

    from pdm.models.candidates import Candidate


class PdmFormatter(argparse.HelpFormatter):
    def start_section(self, heading: str | None) -> None:
        return super().start_section(
            termui.yellow(heading.title() if heading else heading, bold=True)
        )

    def _format_usage(
        self,
        usage: str,
        actions: Iterable[Action],
        groups: Iterable[_ArgumentGroup],
        prefix: str | None,
    ) -> str:
        if prefix is None:
            prefix = "Usage: "
        result = super()._format_usage(usage, actions, groups, prefix)
        if prefix:
            return result.replace(prefix, termui.yellow(prefix, bold=True))
        return result

    def _format_action(self, action: Action) -> str:
        # determine the required width and the entry label
        help_position = min(self._action_max_length + 2, self._max_help_position)
        help_width = max(self._width - help_position, 11)
        action_width = help_position - self._current_indent - 2
        action_header = self._format_action_invocation(action)

        # no help; start on same line and add a final newline
        if not action.help:
            tup = self._current_indent, "", action_header
            action_header = "%*s%s\n" % tup

        # short action name; start on the same line and pad two spaces
        elif len(action_header) <= action_width:
            tup = self._current_indent, "", action_width, action_header  # type: ignore
            action_header = "%*s%-*s  " % tup  # type: ignore
            indent_first = 0

        # long action name; start on the next line
        else:
            tup = self._current_indent, "", action_header  # type: ignore
            action_header = "%*s%s\n" % tup
            indent_first = help_position

        # collect the pieces of the action help
        parts = [termui.cyan(action_header)]

        # if there was help for the action, add lines of help text
        if action.help:
            help_text = self._expand_help(action)
            help_lines = self._split_lines(help_text, help_width)
            parts.append("%*s%s\n" % (indent_first, "", help_lines[0]))
            for line in help_lines[1:]:
                parts.append("%*s%s\n" % (help_position, "", line))

        # or add a newline if the description doesn't end with one
        elif not action_header.endswith("\n"):
            parts.append("\n")

        # if there are any sub-actions, add their help as well
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))

        # return a single string
        return self._join_parts(parts)


class Package:
    """An internal class for the convenience of dependency graph building."""

    def __init__(
        self, name: str, version: str, requirements: dict[str, Requirement]
    ) -> None:
        self.name = name
        self.version = version  # if version is None, the dist is not installed.
        self.requirements = requirements

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"<Package {self.name}=={self.version}>"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Package):
            return False
        return self.name == value.name


def build_dependency_graph(working_set: WorkingSet) -> DirectedGraph:
    """Build a dependency graph from locked result."""
    graph: DirectedGraph[Package | None] = DirectedGraph()
    graph.add(None)  # sentinel parent of top nodes.
    node_with_extras = set()

    def add_package(key: str, dist: Distribution) -> Package:
        name, extras = strip_extras(key)
        extras = extras or ()
        reqs: dict[str, Requirement] = {}
        if dist:
            requirements = (
                Requirement.from_pkg_requirement(r)
                for r in dist.requires(extras)  # type: ignore
            )
            for req in requirements:
                reqs[req.identify()] = req
            version = dist.version
        else:
            version = None

        node = Package(key, version, reqs)
        if node not in graph:
            if extras:
                node_with_extras.add(name)
            graph.add(node)

            for k in reqs:
                child = add_package(
                    k, cast(Distribution, working_set.get(strip_extras(k)[0]))
                )
                graph.connect(node, child)

        return node

    for k, dist in working_set.items():
        add_package(k, dist)
    for node in list(graph):
        if node is not None and not list(graph.iter_parents(node)):
            # Top requirements
            if node.name in node_with_extras:
                # Already included in package[extra], no need to keep the top level
                # non-extra package.
                graph.remove(node)
            else:
                graph.connect(None, node)
    return graph


LAST_CHILD = "└── "
LAST_PREFIX = "    "
NON_LAST_CHILD = "├── "
NON_LAST_PREFIX = "│   "


def format_package(
    graph: DirectedGraph,
    package: Package,
    required: str = "",
    prefix: str = "",
    visited: set[str] | None = None,
) -> str:
    """Format one package.

    :param graph: the dependency graph
    :param package: the package instance
    :param required: the version required by its parent
    :param prefix: prefix text for children
    :param visited: the visited package collection
    """
    if visited is None:
        visited = set()
    result = []
    version = (
        termui.red("[ not installed ]")
        if not package.version
        else termui.red(package.version)
        if required
        and required not in ("Any", "This project")
        and not SpecifierSet(required).contains(package.version)
        else termui.yellow(package.version)
    )
    if package.name in visited:
        version = termui.red("[circular]")
    required = f"[ required: {required} ]" if required else "[ Not required ]"
    result.append(f"{termui.green(package.name, bold=True)} {version} {required}\n")
    if package.name in visited:
        return "".join(result)
    visited.add(package.name)
    children = sorted(graph.iter_children(package), key=lambda p: p.name)
    for i, child in enumerate(children):
        is_last = i == len(children) - 1
        head = LAST_CHILD if is_last else NON_LAST_CHILD
        cur_prefix = LAST_PREFIX if is_last else NON_LAST_PREFIX
        required = str(package.requirements[child.name].specifier or "Any")
        result.append(
            prefix
            + head
            + format_package(
                graph, child, required, prefix + cur_prefix, visited.copy()
            )
        )
    return "".join(result)


def format_reverse_package(
    graph: DirectedGraph,
    package: Package,
    child: Package | None = None,
    requires: str = "",
    prefix: str = "",
    visited: set[str] | None = None,
) -> str:
    """Format one package for output reverse dependency graph."""
    if visited is None:
        visited = set()
    version = (
        termui.red("[ not installed ]")
        if not package.version
        else termui.yellow(package.version)
    )
    if package.name in visited:
        version = termui.red("[circular]")
    requires = (
        f"[ requires: {termui.red(requires)} ]"
        if requires not in ("Any", "")
        and child
        and child.version
        and not SpecifierSet(requires).contains(child.version)
        else ""
        if not requires
        else f"[ requires: {requires} ]"
    )
    result = [f"{termui.green(package.name, bold=True)} {version} {requires}\n"]
    if package.name in visited:
        return "".join(result)
    visited.add(package.name)
    parents: list[Package] = sorted(
        filter(None, graph.iter_parents(package)), key=lambda p: p.name
    )
    for i, parent in enumerate(parents):
        is_last = i == len(parents) - 1
        head = LAST_CHILD if is_last else NON_LAST_CHILD
        cur_prefix = LAST_PREFIX if is_last else NON_LAST_PREFIX
        requires = str(parent.requirements[package.name].specifier or "Any")
        result.append(
            prefix
            + head
            + format_reverse_package(
                graph, parent, package, requires, prefix + cur_prefix, visited.copy()
            )
        )
    return "".join(result)


def _format_forward_dependency_graph(project: Project, graph: DirectedGraph) -> str:
    """Format dependency graph for output."""
    content = []
    all_dependencies = ChainMap(*project.all_dependencies.values())
    for package in sorted(graph.iter_children(None), key=lambda p: p.name):
        if package.name in all_dependencies:
            required = str(all_dependencies[package.name].specifier or "Any")
        elif (
            not project.environment.is_global
            and project.meta.name
            and package.name == project.meta.project_name.lower()
        ):
            required = "This project"
        else:
            required = ""
        content.append(format_package(graph, package, required, "", set()))
    return "".join(content).strip()


def _format_reverse_dependency_graph(
    project: Project, graph: DirectedGraph[Package]
) -> str:
    """Format reverse dependency graph for output."""
    leaf_nodes = sorted(
        (node for node in graph if not list(graph.iter_children(node))),
        key=lambda p: p.name,
    )
    content = [
        format_reverse_package(graph, node, prefix="", visited=set())
        for node in leaf_nodes
    ]
    return "".join(content).strip()


def format_dependency_graph(
    project: Project, graph: DirectedGraph[Package], reverse: bool = False
) -> str:
    if reverse:
        return _format_reverse_dependency_graph(project, graph)
    else:
        return _format_forward_dependency_graph(project, graph)


def format_lockfile(
    mapping: dict[str, Candidate],
    fetched_dependencies: dict[str, list[Requirement]],
    summary_collection: dict[str, str],
) -> dict:
    """Format lock file from a dict of resolved candidates, a mapping of dependencies
    and a collection of package summaries.
    """
    packages = atoml.aot()
    file_hashes = atoml.table()
    for k, v in sorted(mapping.items()):
        base = atoml.table()
        base.update(v.as_lockfile_entry())  # type: ignore
        base.add("summary", summary_collection[strip_extras(k)[0]])
        deps = make_array(sorted(r.as_line() for r in fetched_dependencies[k]), True)
        if len(deps) > 0:
            base.add("dependencies", deps)
        packages.append(base)  # type: ignore
        if v.hashes:
            key = f"{strip_extras(k)[0]} {v.version}"
            if key in file_hashes:
                continue
            array = atoml.array().multiline(True)
            for filename, hash_value in v.hashes.items():
                inline = make_inline_table({"file": filename, "hash": hash_value})
                array.append(inline)  # type: ignore
            if array:
                file_hashes.add(key, array)
    doc = atoml.document()
    doc.add("package", packages)  # type: ignore
    metadata = atoml.table()
    metadata.add("files", file_hashes)
    doc.add("metadata", metadata)  # type: ignore
    return cast(dict, doc)


def save_version_specifiers(
    requirements: dict[str, dict[str, Requirement]],
    resolved: dict[str, Candidate],
    save_strategy: str,
) -> None:
    """Rewrite the version specifiers according to the resolved result and save strategy

    :param requirements: the requirements to be updated
    :param resolved: the resolved mapping
    :param save_strategy: compatible/wildcard/exact
    """
    for reqs in requirements.values():
        for name, r in reqs.items():
            if r.is_named and not r.specifier:
                if save_strategy == "exact":
                    r.specifier = get_specifier(f"=={resolved[name].version}")
                elif save_strategy == "compatible":
                    version = str(resolved[name].version)
                    compatible_version = ".".join((version.split(".") + ["0"])[:2])
                    r.specifier = get_specifier(f"~={compatible_version}")


def check_project_file(project: Project) -> None:
    """Check the existence of the project file and throws an error on failure."""
    if not project.meta:
        raise ProjectError(
            "The pyproject.toml has not been initialized yet. You can do this "
            "by running {}.".format(termui.green("'pdm init'"))
        )


def find_importable_files(project: Project) -> Iterable[tuple[str, Path]]:
    """Find all possible files that can be imported"""
    for filename in (
        "Pipfile",
        "pyproject.toml",
        "requirements.in",
        "requirements.txt",
    ):
        project_file = project.root / filename
        if not project_file.exists():
            continue
        for key, module in FORMATS.items():
            if module.check_fingerprint(project, project_file.as_posix()):
                yield key, project_file


def set_env_in_reg(env_name: str, value: str) -> None:
    """Manipulate the WinReg, and add value to the
    environment variable if exists or create new.
    """
    import winreg

    value = os.path.normcase(value)

    with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as root:
        with winreg.OpenKey(root, "Environment", 0, winreg.KEY_ALL_ACCESS) as env_key:
            try:
                old_value, type_ = winreg.QueryValueEx(env_key, env_name)
                paths = [os.path.normcase(item) for item in old_value.split(os.pathsep)]
                if value in paths:
                    return
            except FileNotFoundError:
                paths, type_ = [], winreg.REG_EXPAND_SZ
            new_value = os.pathsep.join([value] + paths)
            winreg.SetValueEx(env_key, env_name, 0, type_, new_value)


def format_resolution_impossible(err: ResolutionImpossible) -> str:
    causes: list[RequirementInformation] = err.causes
    result = ["Unable to find a resolution that satisfies the following requirements:"]

    for req, parent in causes:
        result.append(
            f"  {req.as_line()} (from {repr(parent) if parent else 'project'})"
        )

    result.append(
        "Please make sure the package names are correct. If so, you can either "
        "loosen the version constraints of these dependencies, or "
        "set a narrower `requires-python` range in the pyproject.tomli."
    )
    return "\n".join(result)


def translate_sections(
    project: Project, default: bool, dev: bool, sections: Iterable[str]
) -> list[str]:
    """Translate default, dev and sections containing ":all" into a list of sections"""
    optional_groups = set(project.meta.optional_dependencies or [])
    dev_groups = set(project.tool_settings.get("dev-dependencies", []))
    sections_set = set(sections)
    if dev is None:
        dev = True
    if sections_set & dev_groups:
        if not dev:
            raise PdmUsageError(
                "--prod is not allowed with dev sections and should be left"
            )
    elif dev:
        sections_set.update(dev_groups)
    if ":all" in sections:
        sections_set.discard(":all")
        sections_set.update(optional_groups)
    if default:
        sections_set.add("default")
    # Sorts the result in ascending order instead of in random order
    # to make this function pure
    invalid_sections = sections_set - set(project.iter_sections())
    if invalid_sections:
        project.core.ui.echo(
            f"Ignoring non-existing sections: {invalid_sections}", fg="yellow", err=True
        )
        sections_set -= invalid_sections
    return sorted(sections_set)


def merge_dictionary(
    target: MutableMapping[Any, Any], input: Mapping[Any, Any]
) -> None:
    """Merge the input dict with the target while preserving the existing values
    properly. This will update the target dictionary in place.
    """
    for key, value in input.items():
        if key not in target:
            target[key] = value
        elif isinstance(value, dict):
            target[key].update(value)
        elif isinstance(value, list):
            target[key].extend(atoml.item(v) for v in value)
