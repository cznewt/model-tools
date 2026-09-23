# Actions

The image carries a set of small scripts in `/actions`, on the `PATH`. They give every renderer
the same shape: point them at a project, name a target, get YAML in `BUILD_PATH`. Makefiles, CI
jobs and the service catalogs call them instead of remembering each tool's flags.

```sh
docker run --rm -v "$PWD":/work -w /work ghcr.io/cznewt/model-tools:latest actions   # list them
docker run --rm ghcr.io/cznewt/model-tools:latest version                            # tool versions
```

Three variables are shared by all of them:

| Variable | Meaning | Default |
|---|---|---|
| `SOURCE_PATH` | the project directory to render | the working directory |
| `BUILD_PATH` | where the rendered YAML is written | `./build` |
| `SOURCE_TARGET` | environment, target, release or instance to render | per action |

Each action prints the tool version, the file it wrote and how many objects are in it. A missing
required variable fails with exit code 2 and the name of the variable.

## Rendering

| Action | Extra variables |
|---|---|
| `helm-chart-render` | `VALUES_FILES`, `NAMESPACE`, `HELM_ARGS` |
| `kustomize-overlay-render` | `KUSTOMIZE_ARGS` |
| `tanka-environment-export` | `TANKA_NAME` for inline environments |
| `cue-package-export` | `CUE_PACKAGE`, `CUE_EXPRESSION` |
| `kcl-module-render` | `KCL_ENTRY`, `KCL_OPTIONS` |
| `timoni-module-build` | `VALUES_FILES`, `NAMESPACE` |
| `ytt-template-render` | `YTT_FILES`, `YTT_VALUES` |
| `kapitan-target-build`, `kapitan-targets-build` | the reveal variants resolve refs |
| `kapitan-inventory-build`, `kapitan-doc-build` | inventory and component docs |
| `kluctl-project-render` | renders a Kluctl project for a target |

## Validating

`manifests-validate` runs kubeconform over `BUILD_PATH` with the Kubernetes schemas and the
datree CRD catalog, so custom resources like `ExternalSecret` validate too. `KUBERNETES_VERSION`
pins the API version, `CRD_SCHEMAS` replaces the catalog.

## Examples

```sh
IMAGE=ghcr.io/cznewt/model-tools:latest
run() { docker run --rm -u "$(id -u):$(id -g)" -v "$PWD":/work -w /work -e HOME=/tmp "$@" $IMAGE; }

run -e SOURCE_PATH=examples/02-helm/web -e SOURCE_TARGET=web -e NAMESPACE=web \
    -e VALUES_FILES=examples/02-helm/values-prod.yaml -e BUILD_PATH=rendered \
    helm-chart-render

run -e SOURCE_PATH=examples/01-kustomize/overlays/prod -e SOURCE_TARGET=prod \
    -e BUILD_PATH=rendered kustomize-overlay-render

run -e SOURCE_PATH=examples/03-tanka -e SOURCE_TARGET=environments/web/prod \
    -e BUILD_PATH=rendered tanka-environment-export

run -e SOURCE_PATH=examples/07-kcl -e KCL_ENTRY=main.k -e KCL_OPTIONS=env=prod \
    -e SOURCE_TARGET=kcl-prod -e BUILD_PATH=rendered kcl-module-render

run -e BUILD_PATH=rendered manifests-validate
```

The companion repository [gitops-renderers](https://github.com/cznewt/gitops-renderers) keeps its
own justfile because each example needs a different pre-step, for example fetching a chart before
Kapitan compiles. The actions are the short path for the common cases.

## Adding one

An action is a shell script in `docker/files/actions/`, executable, with a one-line description on
line 2 (the `actions` listing reads that line) and the variables documented in the header. Source
`/actions/_common` for `require`, `announce`, `prepare_build_path` and `emit`. Keep them cluster
free: rendering and validation only, so they run in CI without credentials.

Gotcha worth keeping: never put a Go template default inside `${VAR:-...}` in bash. The expansion
ends at the first closing brace and the template silently loses its tail, which is how the CRD
schema URL broke the first time.
