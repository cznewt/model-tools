#!/usr/bin/env just --justfile
# Local build of the image the CI publishes to ghcr.io/cznewt/model-tools.

image := "ghcr.io/cznewt/model-tools"
version := `cat VERSION`
build_args := `sed -e 's/#.*//' -e '/^$/d' -e 's/^/--build-arg /' docker/versions.env | tr '\n' ' '`

default:
    @just --list

[doc('Build the image for the host architecture and tag it with VERSION and latest.')]
build:
    docker build {{build_args}} -t {{image}}:{{version}} -t {{image}}:latest docker/

[doc('Build for amd64 and arm64 with buildx (needs qemu binfmt: docker run --privileged --rm tonistiigi/binfmt --install arm64).')]
build-multiarch push="false":
    docker buildx build --platform linux/amd64,linux/arm64 {{build_args}} -t {{image}}:{{version}} -t {{image}}:latest --push={{push}} docker/

[doc('Build the Jupyter overlay on top of the local base image (stages notebooks/ into the context).')]
build-jupyter:
    rm -rf extra/jupyter-model-tools/docker/files/notebooks && mkdir -p extra/jupyter-model-tools/docker/files/notebooks && cp -r notebooks/. extra/jupyter-model-tools/docker/files/notebooks/
    docker build --build-arg MODEL_TOOLS_VERSION={{version}} -t ghcr.io/cznewt/jupyter-model-tools:{{version}} -t ghcr.io/cznewt/jupyter-model-tools:latest extra/jupyter-model-tools/docker/

[doc('Run JupyterLab with the notebooks mounted (http://localhost:8888, token in the log).')]
jupyter:
    docker compose up

[doc('Print every tool version inside the built image.')]
versions:
    docker run --rm {{image}}:{{version}} version

[doc('Shell in the image with the current directory mounted at /work.')]
shell:
    docker run --rm -it -v "$(pwd)":/work -w /work {{image}}:{{version}} bash
