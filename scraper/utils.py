from pathlib import Path


def create_directories():

    project_root = Path(__file__).resolve().parent.parent

    folders = [
        project_root / "data" / "raw",
        project_root / "data" / "processed",
        project_root / "data" / "final",
        project_root / "logs"
    ]

    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)