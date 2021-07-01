#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    os.environ['DB_NAME'] = 'postgres'
    os.environ['DB_USER'] = 'postgres'
    os.environ['DB_HOST'] = 'postgres'
    os.environ['DB_PORT'] = '5432'
    os.environ['DB_OPTIONS'] = '-c search_path=content'
    os.environ['DB_PASSWORD'] = 'postgres'
    os.environ['DB_SECRET_KEY'] = '5bim(!=4f(8m=w6&k%sr)nptmap(cmterf5dojs$ogh)wg879s'
    os.environ['DB_PASSWORD'] = 'postgres'
    os.environ['DJANGO_SUPERUSER_USERNAME'] = 'dd'
    os.environ['DJANGO_SUPERUSER_EMAIL'] = 'dd@dd.dd'
    os.environ['DJANGO_SUPERUSER_PASSWORD'] ='dd'
    main()
