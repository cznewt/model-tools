# AGENTS.md

- This repo is only the image: `docker/Dockerfile`, `docker/versions.env`, `docker/files/actions`,
  `VERSION`. No application code lives here.
- Bump versions in `docker/versions.env` and `VERSION` together; CI on `main` publishes
  `ghcr.io/cznewt/model-tools:<VERSION>` and `:latest` for amd64 and arm64.
- Verify a bump with `just build && just versions` before pushing. Release assets change naming
  between versions (go-jsonnet did in 0.22, jrsonnet moved to deltarocks); check the URL resolves.
- Keep the image root-runnable and rootless-friendly: consumers run it with `--user $(id -u)`.
- Every notebook ends with a `Try it:` prompt; the signposts (`00-start-here.ipynb`, `<track>/00-index.ipynb`) collect them, so regenerate the signposts after adding or renaming a notebook.
- Notebooks are tests: after editing `notebooks/`, run `just test-notebooks <track>` (network needed) before pushing; CI executes all of them after the image build. Keep cells idempotent and cluster-free (no `tk env set`, `tk diff`, `kubectl apply`).
- Actions live in `docker/files/actions/`: source `/actions/_common`, document the variables in the
  header, put the description on line 2, keep them cluster free. Test one by mounting the directory
  over `/actions` in the published image before rebuilding.
- No em dashes in prose.
