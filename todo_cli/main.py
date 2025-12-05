"""
Module principal de la CLI todo-cli.

Ce module définit les commandes principales du gestionnaire de tâches :
- add : ajouter une nouvelle tâche
- list : afficher les tâches
- done : marquer une tâche comme terminée

Il configure également le système de logging et initialise l'application Typer.
"""

import logging
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table

from .logging_config import configure_logging
from .models import Task
from .storage import load_tasks, next_id, save_tasks

# Configure logging once at startup
configure_logging()
logger = logging.getLogger("todo_cli")

app = typer.Typer(help="Gestionnaire de tâches en ligne de commande")
console = Console()


@app.command()
def add(
    title: str = typer.Argument(..., help="Titre de la tâche"),
    description: str = typer.Option("", "--desc", "-d", help="Description"),
    priority: int = typer.Option(3, "--prio", "-p", min=1, max=5),
    deadline: str | None = typer.Option(
        None,
        "--deadline",
        "-l",
        help="Deadline YYYY-MM-DD",
    ),
) -> None:
    """
    Ajouter une nouvelle tâche à la liste.

    Args:
        title (str): Titre de la tâche à ajouter.
        description (str): Description optionnelle de la tâche.
        priority (int): Niveau de priorité (1 à 5).
        deadline (str | None): Deadline au format YYYY-MM-DD.

    Raises:
        typer.BadParameter: Si la date n'est pas au bon format.

    Effets de bord:
        - Charge les tâches existantes.
        - Valide et convertit la deadline.
        - Ajoute une nouvelle tâche.
        - Sauvegarde la liste mise à jour.
        - Écrit un log de niveau INFO.
    """
    logger.debug("Commande add appelée avec title=%s, priority=%s, deadline=%s", title, priority, deadline)
    tasks = load_tasks()

    parsed_deadline: datetime | None = None
    if deadline:
        try:
            parsed_deadline = datetime.fromisoformat(deadline)
        except ValueError:
            logger.warning("Deadline invalide fournie: %s", deadline)
            raise typer.BadParameter("La date doit être au format YYYY-MM-DD")

    task = Task(
        id=next_id(tasks),
        title=title,
        description=description or None,
        priority=priority,
        deadline=parsed_deadline,
    )
    tasks.append(task)
    save_tasks(tasks)

    logger.info(
        "Tâche ajoutée: id=%s, title=%s, priority=%s, deadline=%s",
        task.id,
        task.title,
        task.priority,
        task.deadline,
    )
    console.print(f"[green]Tâche ajoutée ! ID={task.id}[/green]")


@app.command()
def list(
    show_done: bool = typer.Option(
        True,
        "--all/--todo-only",
        help="Afficher les tâches terminées",
    ),
) -> None:
    """
    Afficher la liste des tâches.

    Args:
        show_done (bool): 
            - True : affiche toutes les tâches
            - False : affiche uniquement les tâches non terminées

    Effets de bord:
        - Charge toutes les tâches.
        - Filtre les tâches selon 'show_done'.
        - Affiche un tableau formaté via Rich.
        - Log niveau DEBUG, WARNING ou INFO selon la situation.
    """
    logger.debug("Commande list appelée avec show_done=%s", show_done)
    tasks = load_tasks()
    if not show_done:
        tasks = [t for t in tasks if not t.done]
        logger.debug("Filtrage des tâches non terminées, total=%s", len(tasks))

    if not tasks:
        logger.warning("Aucune tâche à afficher (show_done=%s)", show_done)

    table = Table(title="Liste des tâches")
    table.add_column("ID")
    table.add_column("Titre")
    table.add_column("Priorité")
    table.add_column("Deadline")
    table.add_column("Terminée")

    for t in tasks:
        table.add_row(
            str(t.id),
            t.title,
            str(t.priority),
            t.deadline.strftime("%Y-%m-%d") if t.deadline else "-",
            "✔️" if t.done else "❌",
        )

    logger.info("Affichage de %s tâche(s)", len(tasks))
    console.print(table)


@app.command()
def done(task_id: int) -> None:
    """
    Marquer une tâche comme terminée.

    Args:
        task_id (int): Identifiant de la tâche à marquer comme terminée.

    Effets de bord:
        - Charge les tâches existantes.
        - Met à jour l'attribut 'done' si la tâche est trouvée.
        - Sauvegarde la liste.
        - Affiche un message de confirmation.
        - Log INFO, WARNING ou ERROR selon la situation.
    """
    logger.debug("Commande done appelée avec task_id=%s", task_id)
    tasks = load_tasks()
    for t in tasks:
        if t.id == task_id:
            if t.done:
                logger.warning("Tâche déjà marquée terminée: id=%s", task_id)
            t.done = True
            save_tasks(tasks)
            logger.info("Tâche marquée comme terminée: id=%s", task_id)
            console.print(f"[green]Tâche {task_id} terminée[/green]")
            return

    logger.error("Tâche introuvable pour task_id=%s", task_id)
    console.print(f"[red]Tâche {task_id} introuvable[/red]")


if __name__ == "__main__":
    app()
