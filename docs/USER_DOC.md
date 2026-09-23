# User documentation

Pull `ghcr.io/cznewt/model-tools:<version>` (versions in git tags of `VERSION`) or `:latest`.
Run tools directly (`docker run --rm -v "$PWD":/work -w /work <image> cue vet ./...`) or the
`/actions` helpers, one per renderer plus `manifests-validate`, driven by `SOURCE_PATH`,
`BUILD_PATH` and `SOURCE_TARGET`. `actions` lists them; [ACTIONS.md](ACTIONS.md) has the details.
`version` prints every tool version. Mount your repository and run as your user
(`--user $(id -u):$(id -g)`) so generated files are not root-owned.
