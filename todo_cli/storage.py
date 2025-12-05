import json
import logging
from pathlib import Path
from typing import List

from .models import Task

logger = logging.getLogger("todo_cli")

DEFAULT_DB_PATH = Path.home() / ".todo_cli_tasks.json"


def load_tasks(path: Path = DEFAULT_DB_PATH) -> List[Task]:
    """Load tasks from the JSON file with full logging."""

    if not path.exists():
        logger.warning("Le fichier de tâches n'existe pas : %s — création implicite", path)
        return []

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        logger.critical("Impossible de lire le fichier %s : %s", path, exc)
        raise

    if not content.strip():
        logger.warning("Le fichier de tâches est vide : %s", path)
        return []

    try:
        raw_data = json.loads(content)
    except json.JSONDecodeError as exc:
        logger.error("Erreur JSON dans %s : %s — retour liste vide", path, exc)
        return []

    tasks = [Task(**item) for item in raw_data]
    logger.debug("Chargement réussi : %s tâche(s) chargée(s) depuis %s", len(tasks), path)

    return tasks


def save_tasks(tasks: List[Task], path: Path = DEFAULT_DB_PATH) -> None:
    """Save tasks into a JSON file with logging."""

    data = [t.model_dump() for t in tasks]

    try:
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    except OSError as exc:
        logger.critical("Erreur critique : impossible d'écrire dans %s : %s", path, exc)
        raise

    logger.info("Sauvegarde réussie : %s tâche(s) écrites dans %s", len(tasks), path)


def next_id(tasks: List[Task]) -> int:
    """Compute the next available task ID."""
    new_id = max((t.id for t in tasks), default=0) + 1
    logger.debug("Calcul du prochain ID : %s", new_id)
    return new_id
