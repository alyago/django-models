common_models_employers
=======================

Django models for Employers database.

common_models_employers is a Django app that provides:
1) DB setting
2) DB routing
3) Django models

It doesn't have urls, views or templates. It serves as a thin interface
to access read-only data in employer_pages database.


Adding it to Django site:

1. Add common_models_employers/ folder

2. Modify settings.py:

    - Add this right after DATABASES:
from common_models_employers.settings.databases import EMPLOYERS_DATABASES
DATABASES.update(EMPLOYERS_DATABASES)

    - Add 'common_models_employers.routers.EmployersRouter' to DATABASE_ROUTERS
    
    - Add 'common_models_employers' to INSTALLED_APPS
