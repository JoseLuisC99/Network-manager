from app import MongoDB

class User(MongoDB.Document):
    username = MongoDB.StringField(required=True, unique=True)
    password = MongoDB.StringField(required=True)
    admin = MongoDB.BooleanField(default=False)

    def to_json(self):
        return {'id': str(self.id), 'username': self.username, 'admin': self.admin}

class Router(MongoDB.Document):
    hostname = MongoDB.StringField(required=True)
    ip = MongoDB.StringField(max_length=15, required=True, unique=True)

    def to_json(self):
        return {'id': str(self.id), 'hostname': self.hostname, 'ip': self.ip}

class RouterUser(MongoDB.Document):
    username = MongoDB.StringField(required=True)
    password = MongoDB.StringField(required=True)
    privilege = MongoDB.IntField(required=True)
    router = MongoDB.ReferenceField(Router, required=True)

    def to_json(self):
        return {'id': str(self.id), 'username': self.username, 'privilege': self.privilege, 'router': self.router.to_json()}