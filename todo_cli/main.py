import logging
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table

from .logging_config import configure_logging
from .models import Task
from .storage import load_tasks, next_id, save_tasks

# configuration du logging au démarrage du module
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

    logger.info("Tâche ajoutée: id=%s, title=%s, priority=%s, deadline=%s", task.id, task.title, task.priority, task.deadline)
    console.print(f"[green]Tâche ajoutée ! ID={task.id}[/green]")


@app.command()
def list(
    show_done: bool = typer.Option(
        True,
        "--all/--todo-only",
        help="Afficher les tâches terminées",
    ),
) -> None:
    logger.debug("Commande list appelée avec show_done=%s", show_done)
    tasks = load_tasks()
    if not show_done:
        tasks = [t for t in tasks if not t.done]
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
    logger.debug("Commande done appelée avec task_id=%s", task_id)
    tasks = load_tasks()
    for t in tasks:
        if t.id == task_id:
            if t.done :
                logger.warning("Tâche déjà marquée terminée: id=%s", task_id)
            t.done = True
            save_tasks(tasks)
            logger.info("Tâche marquée comme terminée: id=%s", task_id)
            console.print(f"[green]Tâche {task_id} terminée[/green]")
            return
    logger.error("Tâche introuvable pour task_id=%s", task_id)
    console.print(f"[red]Tâche {task_id} introuvable[/red]")
