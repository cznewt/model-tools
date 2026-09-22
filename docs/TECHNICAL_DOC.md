# Technical documentation

Two-stage Dockerfile on `ubuntu:24.04`: the `downloader` stage installs kapitan into a venv and
downloads every release binary for `TARGETARCH` (amd64 or arm64; jrsonnet and just use their own
architecture spelling, derived in a `case`), the final stage copies the venv and binaries and
installs the runtime packages (git, ssh, curl, libmagic for kapitan, fish for mxc recipes).

`docker/versions.env` is the single list of tool versions; the justfile and the workflow turn it
into `--build-arg`s. `VERSION` is the image tag. `.github/workflows/build-model-tools.yml` runs on
pushes to `main` touching `docker/**` or `VERSION` and on manual dispatch: buildx with QEMU for
arm64, GHA cache, push to ghcr.io, cosign signature.

## Notebooks

`notebooks/<track>/*.ipynb` use the bash kernel; every cell is a shell command so the same steps
work in a terminal. CI stages the tree into the Jupyter overlay; `just test-notebooks` executes every
notebook with papermill inside the overlay image (network required: the tracks clone
gitops-renderers and kapitan-reference into `/source/work`).
