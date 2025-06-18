from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint

import graphviz
from packaging.requirements import Requirement


parser = argparse.ArgumentParser()
parser.add_argument("reqfile", type=str, help="Requirements file in pip-compile output format")
parser.add_argument("--outprefix", type=str, default="out", help="Prefix for output files")
parser.add_argument("--format", type=str, default="png", help="Graphviz render format")


RequirementGroup: tuple[Requirement, tuple[str, ...]]

def _reqgroups_from_file(fn) -> list[RequirementGroup]:
    results = []
    req = None
    inducers = []

    lines = [l.strip() for l in Path(fn).read_text().splitlines()]

    for line in lines:
        if req is None and "==" not in line:
            # ASSUME: before we've seen any requirement, every non-requirement line can be ignored
            continue

        if req and not line:
            # ASSUME: empty line terminates the list if we've seen *any* requirements
            grp = req, tuple(inducers)
            results.append(grp)
            break

        # ASSUME: all requirements lines use == (i.e. we're not handling <=, >=, ~=, !=, etc.)
        if "==" in line:
            r = line.rstrip("\\")

            if req is None:
                # edge case: first requirement in file
                req = Requirement(r)
            else:
                # otherwise, we just moved from one requirement to another, time to add the current requirement
                # and its inducers to the output
                grp = req, tuple(inducers)
                results.append(grp)

                req = Requirement(r)
                inducers.clear()
        else:
            # we're in the section after a requirement that tells us (via comments) what induced this requirement

            if line.startswith("# via"):
                # we may have a single inducer in which case it's all on the same line, branch for that below:
                ind = line.removeprefix("# via").strip()
                if not ind:
                    # not a single-line inducer, list follows, we ignore the separating line
                    continue
            elif not line.startswith("#"):
                # a --hash line or some other continuation of the requirement line that is not part of the Requirement
            else:
                # the line we're on is part of a list of multiple packages preceded by a `# via` line
                ind = line.removeprefix("#").lstrip().replace("(pyproject.toml)", "")
                if ind == req.name:
                    # edge case: sometimes pkg[extra] will be annotated as induced by pkg, it should be safe to
                    # ignore that and avoid introducing cycles to the graph
                    continue

            inducers.append(ind)


    return results


def _graphviz_from_groups(grps: list[RequirementsGroup], *args, **kwargs) -> graphviz.Digraph:
    dot = graphviz.Digraph("requirements-graph", *args, **kwargs)

    # first pass: create all nodes, ignore inducers
    for (req, _) in grps:
        name = req.name

        # TODO: it would be cool to identify first-order dependencies and make cluster subgraphs out of them, so we get
        # a nice little bounding box. I don't think that nodes can belong to multiple clusters, though, so there isn't
        # an obvious way to proceed in that direction.
        ver = list(req.specifier)[0].version
        label = name + ("" if not req.extras else f"[{', '.join(req.extras)}]") + f"\n{ver}"

        dot.node(name, label=label)


    # second pass: create edges indicating what induced each package
    for req, inducers in grps:
        name = req.name
        edges = [(ind_name, name) for ind_name in inducers]

        dot.edges(edges)

    return dot


if __name__ == "__main__":
    args = parser.parse_args()

    groups = _reqgroups_from_file(args.reqfile)

    dot = _graphviz_from_groups(groups, engine='dot')
    dot.attr(
        "graph",
        pack="true",
        rankdir="LR",
#         ranksep="0.2:0.5:1.0:10.0"
    )

    dot.format = args.format
    outfn = dot.render(filename=args.outprefix + ".gv")

    print(f"Rendered graphviz to {outfn!r}")
