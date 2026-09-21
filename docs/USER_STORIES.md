# User stories

- As a platform engineer I want one image with kapitan, tanka, helm, kustomize, cue, timoni, sops
  and friends, so that catalogs, CI jobs and the gitops-renderers examples run the same toolchain.
- As a maintainer I want the image built by GitHub Actions for amd64 and arm64 from a plain
  Dockerfile, so that no local wrapper container or registry login is needed to release.
- As a consumer I want `ghcr.io/cznewt/model-tools:<version>` tags that never move and a `latest`
  that follows `main`, so that pins stay reproducible.
