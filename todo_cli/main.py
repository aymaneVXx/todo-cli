import typer
from rich.console import Console
from rich.table import Table

from .models import Task
from .storage import load_tasks, save_tasks, next_id

app = typer.Typer(help="Gestionnaire de tâches en ligne de commande")
console = Console()


@app.command()
def add(
    title: str = typer.Argument(..., help="Titre de la tâche"),
    description: str = typer.Option("", "--desc", "-d", help="Description"),
    priority: int = typer.Option(3, "--prio", "-p", min=1, max=5),
    deadline: str = typer.Option("", "--deadline", "-l", help="Deadline YYYY-MM-DD"),
):
    tasks = load_tasks()
    task = Task(
        id=next_id(tasks),
        title=title,
        description=description or None,
        priority=priority,
        deadline=deadline or None,
    )
    tasks.append(task)
    save_tasks(tasks)
    console.print(f"[green]Tâche ajoutée ! ID={task.id}[/green]")


@app.command()
def list(show_done: bool = typer.Option(True, "--all/--todo-only", help="Afficher les tâches terminées")):
    tasks = load_tasks()
    if not show_done:
        tasks = [t for t in tasks if not t.done]

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

    console.print(table)


@app.command()
def done(task_id: int):
    tasks = load_tasks()
    for t in tasks:
        if t.id == task_id:
            t.done = True
            save_tasks(tasks)
            console.print(f"[green]Tâche {task_id} terminée[/green]")
            return

    console.print(f"[red]Tâche {task_id} introuvable[/red]")
