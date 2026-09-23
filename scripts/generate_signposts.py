#!/usr/bin/env python3
"""Regenerate notebooks/00-start-here.ipynb and each track index from the notebooks themselves."""
import json, pathlib

TRACKS = [
 ("introduction", "Introduction", "The talk's walk: one workload in Kustomize, Helm, Tanka, Kapitan, CUE and Timoni, the secret patterns, and the cross-renderer comparison."),
 ("kustomize", "Kustomize", "Bases and overlays, strategic merge and JSON patches, generators, components and replacements, Helm charts inside Kustomize."),
 ("helm", "Helm", "Chart anatomy, values as the chart API, dependencies and OCI, linting, schema validation and secrets through vals."),
 ("jsonnet-tanka", "Jsonnet with Tanka", "A project from tk init: environments, jsonnet-bundler, charts and Kustomize inside Tanka, inline environments and tests."),
 ("jsonnet-kapitan", "Jsonnet with Kapitan", "The official kapitan-reference setup: the inventory, the Kubernetes generator, refs, jinja2 scripts and docs, validation."),
 ("cue", "CUE", "Values, types and constraints, validating rendered manifests, contexts and rendering, Timoni modules and bundles, the mxc fleet model."),
 ("kcl", "KCL", "Schemas with check rules, kcl vet against plain data, kcl test, and the KCL renderer in the companion repository."),
 ("ytt", "ytt", "Carvel's structural templating: data values, Starlark annotations and overlays that patch YAML nodes instead of text."),
 ("kluctl", "Kluctl", "A project with targets and Jinja2 over Kustomize, rendered offline the way CI does it."),
]

def read(nb):
    d = json.loads(nb.read_text())
    title, summary, exercises = nb.stem, "", []
    for c in d["cells"]:
        src = "".join(c["source"])
        if c["cell_type"] != "markdown":
            continue
        if not summary:
            lines = [l for l in src.splitlines() if l.strip()]
            if lines and lines[0].startswith("#"):
                title = lines[0].lstrip("# ").strip()
                body = " ".join(lines[1:])
                summary = (body.split(". ")[0] + ".") if body else ""
        for line in src.splitlines():
            s = line.strip()
            for lead in ("Try it:", "Discussion:"):
                if s.startswith(lead):
                    exercises.append(s[len(lead):].strip())
    return title, summary, exercises

def card(href, label, title, summary):
    return (f'  <a href="{href}" style="display:block;border:1px solid #8886;border-radius:6px;'
            f'padding:12px 14px;text-decoration:none;color:inherit">\n'
            f'    <div style="font-family:ui-monospace,SFMono-Regular,monospace;font-size:.72em;'
            f'letter-spacing:.14em;text-transform:uppercase;opacity:.6">{label}</div>\n'
            f'    <div style="font-weight:600;margin:.25em 0 .4em">{title}</div>\n'
            f'    <div style="font-size:.9em;opacity:.8;line-height:1.35">{summary}</div>\n'
            f'  </a>')

def grid(cards):
    return ('<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:12px">\n'
            + "\n".join(cards) + "\n</div>")

def notebook(cells):
    return json.dumps({"nbformat": 4, "nbformat_minor": 5,
        "metadata": {"kernelspec": {"name": "bash", "display_name": "Bash", "language": "bash"},
                     "language_info": {"name": "bash", "codemirror_mode": "shell", "mimetype": "text/x-sh", "file_extension": ".sh"}},
        "cells": [{"cell_type": "markdown", "metadata": {}, "source": s.strip("\n") + "\n"} for s in cells]}, indent=1) + "\n"

root_cards, total, all_ex = [], 0, 0
for folder, title, desc in TRACKS:
    d = pathlib.Path("notebooks", folder)
    nbs = sorted(p for p in d.glob("*.ipynb") if not p.name.startswith("00-index"))
    total += len(nbs)
    cards, exercises = [], []
    for nb in nbs:
        t, summary, ex = read(nb)
        cards.append(card(nb.name, nb.stem.split("-")[0], t, summary))
        if ex:
            exercises.append((t, nb.name, ex)); all_ex += len(ex)
    cells = [f"# {title}\n\n{desc}\n\nEvery cell is a shell command, so the same steps work in a terminal. Run the notebooks in order; `/source/work` survives restarts.",
             grid(cards)]
    if exercises:
        blocks = ["## Exercises\n\nThe prompts left in the notebooks, in one place."]
        for t, name, ex in exercises:
            blocks.append(f"**[{t}]({name})**\n\n" + "\n".join(f"- {e}" for e in ex))
        cells.append("\n\n".join(blocks))
    cells.append("[Back to all tracks](../00-start-here.ipynb)")
    (d / "00-index.ipynb").write_text(notebook(cells))
    root_cards.append(card(f"{folder}/00-index.ipynb", f"{len(nbs)} notebook" + ("s" if len(nbs) != 1 else ""), title, desc))

pathlib.Path("notebooks/00-start-here.ipynb").write_text(notebook([
 "# model-tools notebooks\n\nOne track per renderer, plus the introduction that walks all of them. Pick a card.",
 grid(root_cards),
 ("## How to run\n\nThe kernel is **Bash**: every cell is a shell command, and the tools come from this image "
  "(`version` prints them, `actions` lists the render helpers). Work happens in `/source/work`, which is the "
  "only directory that survives a restart; `/source/notebooks` is seeded from the image on first start, so your "
  "edits stay.\n\nThe tracks clone two repositories into `/source/work`: "
  "[gitops-renderers](https://github.com/cznewt/gitops-renderers) for the examples and "
  "[kapitan-reference](https://github.com/kapicorp/kapitan-reference) for the Kapitan track. Network is needed "
  "the first time.\n\nEach track ends with exercises, collected on its own card page.")
]))
print(f"{total} notebooks, {all_ex} exercises, {len(TRACKS)} tracks")
