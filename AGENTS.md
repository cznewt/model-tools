# AGENTS.md

- This repo is only the image: `docker/Dockerfile`, `docker/versions.env`, `docker/files/actions`,
  `VERSION`. No application code lives here.
- Bump versions in `docker/versions.env` and `VERSION` together; CI on `main` publishes
  `ghcr.io/cznewt/model-tools:<VERSION>` and `:latest` for amd64 and arm64.
- Verify a bump with `just build && just versions` before pushing. Release assets change naming
  between versions (go-jsonnet did in 0.22, jrsonnet moved to deltarocks); check the URL resolves.
- Keep the image root-runnable and rootless-friendly: consumers run it with `--user $(id -u)`.
- No em dashes in prose.
