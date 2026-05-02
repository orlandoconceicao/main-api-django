#!/usr/bin/env python
import os
import sys

import os
print("ROOT DIR:", os.getcwd())
print("FILES:", os.listdir("."))
print("SOFTWARE:", os.listdir("software_sales") if os.path.exists("software_sales") else "NOT FOUND")

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "software_sales.core.settings")
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
    main()