# model-tools

One container image with every "desired state" renderer and its helpers, built by GitHub Actions
for amd64 and arm64 and published as `ghcr.io/cznewt/model-tools:<version>` (see `VERSION`).

| Tools | Purpose |
|---|---|
| kapitan, jsonnet, jsonnetfmt, jsonnet-lint, jb, jrsonnet, tk | Jsonnet: Kapitan inventory compiles, Tanka environments, jsonnet-bundler |
| helm, kustomize, kubectl, kubeconform | Helm charts, Kustomize overlays, server-side dry runs, schema validation |
| cue, timoni, kcl, ytt, kluctl | CUE packages and Timoni modules, KCL, ytt, Kluctl deployments |
| flux, argocd, argo | GitOps engine clients: Flux, Argo CD and Argo Workflows, for reconciling and inspecting what the renderers produced |
| sops, age, vals | Secrets in Git (SOPS + age), secret references (`ref+vault://`, `ref+sops://`, ...) |
| yq, jq, just, fish | Glue (fish because mxc's just recipes use it) |

```sh
docker run --rm ghcr.io/cznewt/model-tools:latest version      # every tool version
docker run --rm -v "$PWD":/work -w /work ghcr.io/cznewt/model-tools:latest kustomize build overlays/prod
```

## Actions

`/actions` gives every renderer the same shape: point a script at a project, name a target, get
YAML in `BUILD_PATH`. `actions` lists them, `version` prints the tool versions, and
[docs/ACTIONS.md](docs/ACTIONS.md) documents the variables.

| Renderer | Action |
|---|---|
| Helm | `helm-chart-render` |
| Kustomize | `kustomize-overlay-render` |
| Jsonnet, Tanka | `tanka-environment-export` |
| Jsonnet, Kapitan | `kapitan-target-build`, `kapitan-targets-build`, the `-reveal-` variants, `kapitan-inventory-build`, `kapitan-doc-build` |
| CUE | `cue-package-export` |
| Timoni | `timoni-module-build` |
| KCL | `kcl-module-render` |
| ytt | `ytt-template-render` |
| Kluctl | `kluctl-project-render` |
| any | `manifests-validate` (kubeconform with the CRD catalog) |

```sh
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD":/work -w /work -e HOME=/tmp \
  -e SOURCE_PATH=examples/02-helm/web -e SOURCE_TARGET=web -e BUILD_PATH=rendered \
  ghcr.io/cznewt/model-tools:latest helm-chart-render
```

Companion examples: [cznewt/gitops-renderers](https://github.com/cznewt/gitops-renderers).

## Jupyter overlay

`ghcr.io/cznewt/jupyter-model-tools` is JupyterLab on top of the base image (bash kernel, language
servers for Jsonnet, YAML, JSON and shell, fish terminal) with the `notebooks/` tree seeded into
`/source/notebooks` on first start. Open `00-start-here.ipynb`: it is a signpost of cards, one per
track, and each track has its own `00-index.ipynb` with a card per notebook and the track's
exercises collected at the bottom.

| Folder | Notebooks |
|---|---|
| `introduction/` | the talk's walk through Kustomize, Helm, Tanka, Kapitan, CUE and Timoni, secrets patterns and the cross-renderer comparison, against [gitops-renderers](https://github.com/cznewt/gitops-renderers) |
| `jsonnet-tanka/` | a Tanka project from `tk init`: environments, jsonnet-bundler and k8s-libsonnet, Helm charts and Kustomize inside Tanka, inline environments, linting and testing |
| `jsonnet-kapitan/` | the official [kapitan-reference](https://github.com/kapicorp/kapitan-reference) setup: inventory and classes, the Kubernetes generator, refs and secrets, jinja2 scripts and docs, validation and testing |
| `cue/` | CUE from scratch: values, types and constraints; importing YAML and validating rendered manifests with `cue vet`; contexts and `cue cmd` rendering in the companion repo; Timoni modules and bundles; the mxc fleet model |
| `helm/` | chart anatomy from `helm create`, values layering and `values.schema.json`, dependencies and OCI, lint, kubeconform, environment diffs and secrets through vals |
| `kustomize/` | bases and overlays with `kustomize edit`, strategic merge and JSON patches, generators, components and replacements, Helm charts inside Kustomize, validation |
| `ytt/` | Carvel's ytt: data values, Starlark annotations, overlays that patch by matching YAML nodes |
| `kcl/` | KCL schemas with `check:` rules, `kcl vet` and `kcl test`, ending on the companion repo's KCL renderer |
| `kluctl/` | a Kluctl project: targets, Jinja2 templating over Kustomize, offline rendering |

```sh
docker compose up            # http://localhost:8888, token in the log; ./work is persistent
helm install lab oci://ghcr.io/cznewt/charts/jupyter-model-tools --set persistence.enabled=true
```

Layout follows monitor-tools: `extra/jupyter-model-tools/docker` (overlay image),
`notebooks/` (baked in by CI), `charts/jupyter-model-tools` (published to `oci://ghcr.io/cznewt/charts`).

Tests: `just test-notebooks [track]` executes the notebooks with papermill inside the overlay
(every cell is a shell command, so a failing command fails the notebook); CI runs the same after
each image build, and the smoke job checks that every tool in the base image answers.

## Releasing

1. Bump tool versions in `docker/versions.env`, bump `VERSION` (`YYYY.M-rN`).
2. Push to `main`: the `Build model-tools` workflow builds both architectures with buildx, pushes
   `ghcr.io/cznewt/model-tools:<VERSION>` and `:latest`, and signs the digest with cosign.
3. `just build` / `just versions` reproduce the amd64 image locally without any wrapper container.

This repository replaces the `cicd-tools/model-tools` entry of the cicd-services catalog, which was
built through the docker-tools wrapper and published to Docker Hub.
