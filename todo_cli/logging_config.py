import logging
from pathlib import Path

LOG_DIR = Path.home() / ".todo_cli"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "todo-cli.log"


def configure_logging(level: int = logging.INFO) -> None:
    """Configure global logging for the todo_cli package."""
    logger = logging.getLogger("todo_cli")
    logger.setLevel(level)

    if logger.handlers:
        return

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # logs vers un fichier
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # logs vers la console (stderr)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
