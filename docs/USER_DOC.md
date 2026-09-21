# User documentation

Pull `ghcr.io/cznewt/model-tools:<version>` (versions in git tags of `VERSION`) or `:latest`.
Run tools directly (`docker run --rm -v "$PWD":/work -w /work <image> cue vet ./...`) or the
`/actions` helpers used by Kapitan catalogs (`SOURCE_PATH`, `BUILD_PATH`, `SOURCE_TARGET` env vars).
`version` prints every tool version. Mount your repository and run as your user
(`--user $(id -u):$(id -g)`) so generated files are not root-owned.
