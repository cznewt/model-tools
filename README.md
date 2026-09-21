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

## Releasing

1. Bump tool versions in `docker/versions.env`, bump `VERSION` (`YYYY.M-rN`).
2. Push to `main`: the `Build model-tools` workflow builds both architectures with buildx, pushes
   `ghcr.io/cznewt/model-tools:<VERSION>` and `:latest`, and signs the digest with cosign.
3. `just build` / `just versions` reproduce the amd64 image locally without any wrapper container.

This repository replaces the `cicd-tools/model-tools` entry of the cicd-services catalog, which was
built through the docker-tools wrapper and published to Docker Hub.
