# Static Code Analysis 

## Outils
Le projet utilise deux outils d'analyse statique :

- **Ruff** : linting, style, tri des imports  
- **Mypy** : vérification statique des types

Ces dépendances sont déclarées dans `pyproject.toml` dans la section `[tool.poetry.dev-dependencies]`.

## Installation

Les outils sont installés via Poetry :

```bash
poetry add -D ruff mypy
```
# Configuration:
La configuration se trouve dans le fichier `pyproject.toml`, via le lien suivant :
https://github.com/aymaneVXx/todo-cli/blob/main/pyproject.toml

# Exécution
Analyse Ruff :
```bash
poetry run ruff check .
```
Auto-format :
```bash
poetry run ruff check . --fix
```
Analyse de types Mypy :
```bash
poetry run mypy todo_cli
```

