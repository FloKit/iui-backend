# iui-backend

## Set up the environment
1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Set up the environment:
```bash
make env 
```

## Set up jupyter kernel within poetry
```bash
poetry run python -m ipykernel install --user --name pyiui_backend
```

## Start environment and start server
```bash
poetry shell
```
```bash
python server.py
```

## Install dependencies
To install all dependencies for this project, run:
```bash
poetry install
```

To install a new package, run:
```bash
poetry add <package-name>
```