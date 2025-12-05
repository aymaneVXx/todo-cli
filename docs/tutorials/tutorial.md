# Tutoriel : Bien démarrer avec todo-cli

Ce tutoriel vous guide pas à pas pour utiliser **todo-cli**, un gestionnaire de tâches en ligne de commande écrit en Python.

---

## 🛠️ Installation

Assurez-vous d’avoir :

- Python 3.10+
- Poetry installé

Clonez le projet :

```bash
git clone https://github.com/aymaneVXx/todo-cli
cd todo-cli
```
Installez les dépendances :
```bash
poetry install
```

## 🚀 Lancer l'application :
Toutes les commandes s’exécutent via :
```bash
poetry run python -m todo_cli.main
```
### 📝 Ajouter une tâche :
Exemple :
```bash
poetry run python -m todo_cli.main add "Faire les courses" -p 4 -l 2025-01-10
```
Options disponibles :

| Option               | Description                   |
| -------------------- | ----------------------------- |
| `--desc` ou `-d`     | Description de la tâche       |
| `--prio` ou `-p`     | Priorité (1–5)                |
| `--deadline` ou `-l` | Deadline au format YYYY-MM-DD |

### 📝 lister les tâches :
Toutes les tâches :
```bash
poetry run python -m todo_cli.main list
```

Uniquement les tâches non terminées :
```bash
poetry run python -m todo_cli.main list --todo-only
```
### 📝 Marquer une tâche comme terminée :
Avec l’ID de la tâche :
```bash
poetry run python -m todo_cli.main done 1
```
### 📁 Où sont stockées les tâches ? 
Les tâches sont enregistrées automatiquement dans :

```bash
~/.todo_cli_tasks.json
```

C’est un simple fichier JSON lisible et modifiable.

### 🧪 Lancer les tests

```bash
poetry run pytest
```
Les tests vérifient notamment :
- le parsing des dates
- la sauvegarde JSON
- la génération des IDs

### 📚 Aller plus loin

- Consultez les docstrings dans le code pour comprendre l’implémentation
- La documentation générique est disponible dans : docs/build/index.html

### 🎉 Félicitations !

Vous savez maintenant installer, lancer et utiliser **todo-cli** !