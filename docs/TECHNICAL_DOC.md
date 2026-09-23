# Technical documentation

Two-stage Dockerfile on `ubuntu:24.04`: the `downloader` stage installs kapitan into a venv and
downloads every release binary for `TARGETARCH` (amd64 or arm64; jrsonnet and just use their own
architecture spelling, derived in a `case`), the final stage copies the venv and binaries and
installs the runtime packages (git, ssh, curl, libmagic for kapitan, fish for mxc recipes).

`docker/versions.env` is the single list of tool versions; the justfile and the workflow turn it
into `--build-arg`s. `VERSION` is the image tag. `.github/workflows/build-model-tools.yml` runs on
pushes to `main` touching `docker/**` or `VERSION` and on manual dispatch: buildx with QEMU for
arm64, GHA cache, push to ghcr.io, cosign signature.

## Actions

`docker/files/actions/` is copied to `/actions` and added to the `PATH`. `_common` holds `require`,
`announce`, `prepare_build_path` and `emit`; every other file is one action whose second line is
its description, which `actions` prints. They render and validate only, never talk to a cluster.

## Notebooks

`notebooks/00-start-here.ipynb` and each track's `00-index.ipynb` are generated signposts: markdown
cards linking to the notebooks, plus the `Try it:` prompts collected as the track's exercises. Adding
or renaming a notebook means regenerating them. `notebooks/<track>/*.ipynb` use the bash kernel; every cell is a shell command so the same steps
work in a terminal. CI stages the tree into the Jupyter overlay; `just test-notebooks` executes every
notebook with papermill inside the overlay image (network required: the tracks clone
gitops-renderers and kapitan-reference into `/source/work`).
