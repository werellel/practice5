class MultiDBRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'auth':
            return 'auth_db'
        return 'default'
        
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'auth':
            return 'auth_db'
        return 'default'

    def allow_migrate(self, db, model):
        if db == 'auth_db':
            if model._meta.app_label == 'auth':
                return True
            else:
                return False
        return True