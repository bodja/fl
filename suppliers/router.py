class SuppliersRouter(object):
    """
    A router to control all database operations on models in the
    suppliers application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read suppliers models go to suppliers_db.
        """
        if model._meta.app_label == 'suppliers':
            return 'suppliers_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write suppliers models go to suppliers_db.
        """
        if model._meta.app_label == 'suppliers':
            return 'suppliers_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the suppliers app is involved.
        """
        if obj1._meta.app_label == 'suppliers' or \
                obj2._meta.app_label == 'suppliers':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the suppliers app only appears in the 'suppliers_db'
        database.
        """
        if app_label == 'suppliers':
            return db == 'suppliers_db'
        return None
