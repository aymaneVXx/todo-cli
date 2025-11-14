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