# model-tools

One container image with every "desired state" renderer and its helpers, built by GitHub Actions
for amd64 and arm64 and published as `ghcr.io/cznewt/model-tools:<version>` (see `VERSION`).

| Tools | Purpose |
|---|---|
| kapitan, jsonnet, jsonnetfmt, jsonnet-lint, jb, jrsonnet, tk | Jsonnet: Kapitan inventory compiles, Tanka environments, jsonnet-bundler |
| helm, kustomize, kubectl, kubeconform | Helm charts, Kustomize overlays, server-side dry runs, schema validation |
| cue, timoni, kcl, ytt, kluctl | CUE packages and Timoni modules, KCL, ytt, Kluctl deployments |
| sops, age, vals | Secrets in Git (SOPS + age), secret references (`ref+vault://`, `ref+sops://`, ...) |
| yq, jq, just, fish | Glue (fish because mxc's just recipes use it) |

```sh
docker run --rm ghcr.io/cznewt/model-tools:latest version      # every tool version
docker run --rm -v "$PWD":/work -w /work ghcr.io/cznewt/model-tools:latest kustomize build overlays/prod
```

`/actions` holds the Kapitan helpers used by the service catalogs (`kapitan-target-build`,
`kapitan-targets-build`, `kapitan-inventory-build`, `kapitan-doc-build`, `kluctl-project-render`,
`version`). Companion examples: [cznewt/gitops-renderers](https://github.com/cznewt/gitops-renderers).

## Jupyter overlay

`ghcr.io/cznewt/jupyter-model-tools` is JupyterLab on top of the base image (bash kernel, language
servers for Jsonnet, YAML, JSON and shell, fish terminal) with the `notebooks/` tree seeded into
`/source/notebooks` on first start:

| Folder | Notebooks |
|---|---|
| `introduction/` | the talk's walk through Kustomize, Helm, Tanka, Kapitan, CUE and Timoni, secrets patterns and the cross-renderer comparison, against [gitops-renderers](https://github.com/cznewt/gitops-renderers) |
| `jsonnet-tanka/` | a Tanka project from `tk init`: environments, jsonnet-bundler and k8s-libsonnet, Helm charts and Kustomize inside Tanka, inline environments, linting and testing |
| `jsonnet-kapitan/` | the official [kapitan-reference](https://github.com/kapicorp/kapitan-reference) setup: inventory and classes, the Kubernetes generator, refs and secrets, jinja2 scripts and docs, validation and testing |

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
