# jupic-toolkit
JupIC toolkit

## Run 
```shell
$ make run
```

## Install
```shell
$ poetry install
```

## Package
Bump version with Poetry (or manually in `pyproject.toml`), 
```shell
$ poetry version (patch|minor|major)
```

Then:
```shell
$ make package
```