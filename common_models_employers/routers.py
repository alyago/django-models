
class EmployersRouter(object):
    """
    A router to control all database operations on models in the common_models_employers app.
    
    Add to settings.py of your site:
    DATABASE_ROUTERS = ['common_models_employers.routers.EmployersRouter']
    """
    def __init__(self):
        self.db = 'employers'
        self.app_label = 'common_models_employers'

    def db_for_read(self, model, **hints):
        """
        Attempts to read employers models go to emp_db.
        """
        if model._meta.app_label == self.app_label:
            return self.db
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write employers models go to emp_db.
        """
        if model._meta.app_label == self.app_label:
            return self.db
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow any relation if both models are in employers app.
        """
        if obj1._meta.app_label == self.app_label and obj2._meta.app_label == self.app_label:
            return True

        # No opinion if both models are not in employers app.
        elif self.app_label not in [obj1._meta.app_label, obj2._meta.app_label]:
            return None

        # Disallow if one in employers and the other not.
        else:
            return False

    def allow_syncdb(self, db, model):
        """
        employers app models appear only in emp_db
        """
        if db == self.db and model._meta.app_label == self.app_label:
            return True
        elif db != self.db and model._meta.app_label != self.app_label:
            return None
        else:
            return False
