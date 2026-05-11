#!/usr/bin/env python
"""Root Django launcher for deployment platforms that invoke manage.py from repo root."""
from pathlib import Path
import os
import sys


def main():
    project_root = Path(__file__).resolve().parent / "WellPath"
    sys.path.insert(0, str(project_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WellPath.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
