class AuthRouter:
    route_app_labels = {'users', 'admin', 'contenttypes', 'sessions'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'users'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'users'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        '''
        this will make user all relationship in this database
        is between the apps in the route_app_labels
        '''
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
            ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        '''
        this function is to make sure the data goes to the appropriate
        database during migrations
        '''
        if app_label in self.route_app_labels:
            return db == 'users'
        return None