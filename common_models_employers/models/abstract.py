# Model in sub-directory via app_label:
# http://stackoverflow.com/questions/2480060/model-in-sub-directory-via-app-label
# https://groups.google.com/forum/#!topic/django-users/MmaiKvbDlDc

from django.db import models

class AbstractEmployer(models.Model):
    class Meta:
        abstract = True
        app_label = 'common_models_employers'
