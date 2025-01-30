# notebook-gena

[![Release](https://img.shields.io/github/v/release/rajeshpv/notebook-gena)](https://img.shields.io/github/v/release/rajeshpv/notebook-gena)
[![Build status](https://img.shields.io/github/actions/workflow/status/rajeshpv/notebook-gena/main.yml?branch=main)](https://github.com/rajeshpv/notebook-gena/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/rajeshpv/notebook-gena)](https://img.shields.io/github/commit-activity/m/rajeshpv/notebook-gena)
[![License](https://img.shields.io/github/license/rajeshpv/notebook-gena)](https://img.shields.io/github/license/rajeshpv/notebook-gena)

This is a template repository for Python projects that use uv for their dependency management.

## VSCode settings

```bash
mkdir -p .vscode
echo '{"explorer.excludeGitIgnore": true}' > .vscode/settings.json
```

## Features

### Makefiles changes

#### Run particular test-file under watch mode

```bash
cd $HOME/projects/github/notebook-gena

make test-watch FILENAME=tests/test_foo.py
make test-watch FILENAME=tests/test_mongodb.py
make test-watch FILENAME=tests/test_postgresdb.py
```
