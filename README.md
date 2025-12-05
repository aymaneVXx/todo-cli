# todo-cli

Un gestionnaire de tâches en ligne de commande écrit en Python.  
Ce projet a pour objectif de démontrer l'utilisation d'un **build tool moderne** :  
 **Poetry**, pour la gestion des dépendances, le packaging, la gestion des versions et l’automatisation du workflow.

---

# Fonctionnalités

- Ajouter une tâche avec titre, description, priorité et deadline.
- Lister les tâches avec un affichage propre (Rich).
- Marquer une tâche comme terminée.
- Validation des données via Pydantic.
- Persistance des tâches dans un fichier JSON (`~/.todo_cli_tasks.json`).

---

# Build Tool utilisé : Poetry

Ce projet utilise **Poetry** pour automatiser :

- la **gestion des dépendances**
- la **création d’un environnement virtuel**
- l’**exécution du programme**
- la **gestion de version**
- le **packaging** (génération de wheels)
- le **lancement des tests**

Cela rend le projet **reproductible** avec de simples commandes.

---

# Installation du projet

Pré-requis :

- Python 3.10+
- Poetry installé (`sudo apt install python3-poetry` ou via le script officiel)

Installation du projet :
`poetry install`

Poetry :
- crée un environnement virtuel isolé
- installe automatiquement toutes les dépendances déclarées dans pyproject.toml

# Utilisation
- Ajouter une tâche:
 `poetry run python -m todo_cli.main add "Faire le TP" -p 4 -l 2025-01-10`

- Lister les tâches:
 `poetry run python -m todo_cli.main list`

- Lister uniquement les tâches non terminées:
 `poetry run python -m todo_cli.main list --todo-only`

- Marquer une tâche comme terminée:
 `poetry run python -m todo_cli.main done 1`


Les tâches sont enregistrées dans un fichier JSON caché :
~/.todo_cli_tasks.json

# Lancer les tests:

Les tests unitaires utilisent **pytest** :
 `poetry run pytest`


Ils couvrent :
- le parsing des dates dans le modèle Task
- la sauvegarde/lecture du fichier JSON
- la génération automatique des IDs

# Build / Packaging:

Pour générer les artefacts du projet (Wheel + source archive) :
`poetry build`

Les fichiers sont donc générés dans le dossier : `dist`.

# Journalisation (Logging)

Le projet utilise le module standard Python `logging` pour tracer l’exécution de la CLI.

## Configuration

La configuration est **centralisée** dans le fichier :
`todo_cli/logging_config.py`

* **Logger principal :** `todo_cli`

## Niveaux de Log

Les niveaux de sévérité suivants sont utilisés pour catégoriser les messages :

* **DEBUG** : Détails techniques pour le développement (appels de commandes, paramètres reçus, logique de filtrage).
* **INFO** : Opérations réussies (tâche ajoutée, liste affichée, tâche marquée comme terminée).
* **WARNING** : Situations inattendues mais gérées ou erreurs utilisateur (ex : entrée invalide, deadline incorrecte, tentative de terminer une tâche déjà close).
* **ERROR** : Problèmes empêchant une fonction de s'exécuter (ex : tâche introuvable par ID, erreurs système graves).

## Destinations des Logs (Outputs)

Les logs sont envoyés simultanément vers deux destinations :

1. **Fichier rotatif :**
   `~/.todo_cli/todo-cli.log`
2. **Sortie standard (Console) :**
   Affichage direct dans le terminal.

## Initialisation

La configuration est appliquée au démarrage de l'application dans `todo_cli/main.py`.

```python
from .logging_config import configure_logging
configure_logging()
```
## Hooks pre-commit

L’exécution de **Ruff** et **Mypy** est automatisée via `pre-commit`.
Le fichier de configuration se trouve à la racine du projet :

`.pre-commit-config.yaml`

### Installation de pre-commit et activation du hook

```bash
poetry run pre-commit install
```
Cela installe un hook Git dans .git/hooks/pre-commit qui se lance automatiquement à chaque commit.
### Lancer les hooks manuellement
```bash
poetry run pre-commit run --all-files
```
Si Ruff ou Mypy détectent des problèmes, le commit est bloqué tant que le code n’est pas corrigé.

# Analyse statique du code

Ce projet utilise deux outils d’analyse statique :

- **Ruff** : linting, style, tri des imports
- **Mypy** : vérification statique des types

Ces outils sont déclarés dans `pyproject.toml` dans la section `[tool.poetry.dev-dependencies]`.

### Installation (déjà gérée par Poetry)

Les dépendances de dev sont installées avec :

```bash
poetry install
```
## Lancer l’analyse statique

### Analyse Ruff

```bash
poetry run ruff check .
```
### Auto-fix
```bash
poetry run ruff check . --fix
```
### Analyse de types avec Mypy
```bash
poetry run mypy todo_cli
```
# Licence

Ce projet est distribué sous la licence **MIT**.  
Vous pouvez consulter les détails dans le fichier [`LICENSE`](LICENSE).
