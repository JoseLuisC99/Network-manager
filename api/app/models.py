from app import MongoDB
from flask_mongoengine import QuerySet

class User(MongoDB.Document):
    username = MongoDB.StringField(required=True, unique=True)
    password = MongoDB.StringField(required=True)
    admin = MongoDB.BooleanField(default=True)

    def to_json(self):
        return {'id': str(self.id), 'username': self.username, 'admin': self.admin}

class Router(MongoDB.Document):
    hostname = MongoDB.StringField(required=True, unique=True)
    ip = MongoDB.StringField(max_length=15, required=True, unique=True)
    description = MongoDB.StringField()
    contact = MongoDB.StringField()
    location = MongoDB.StringField()

    def to_json(self):
        return {'id': str(self.id), 'hostname': self.hostname, 'ip': self.ip, 'description': self.description, 'contact': self.contact, 'location': self.location}
    
    @classmethod
    def sort_by_ip(_, queryset, reverse=False):
        if not isinstance(queryset, QuerySet):
            raise TypeError('order requires a QuerySet instance')
        def split_ip(ip):
            return tuple(int(part) for part in ip.split('.'))
        return sorted(queryset, key=lambda obj: split_ip(obj.ip), reverse=reverse)

class RouterUser(MongoDB.Document):
    username = MongoDB.StringField(required=True)
    password = MongoDB.StringField(required=True)
    privilege = MongoDB.IntField(required=True)
    router = MongoDB.ReferenceField(Router, required=True, reverse_delete_rule=MongoDB.CASCADE)

    def to_json(self):
        return {'id': str(self.id), 'username': self.username, 'privilege': self.privilege, 'router': self.router.to_json()}

class Interface(MongoDB.Document):
    description = MongoDB.StringField(required=True)
    status = MongoDB.BooleanField(required=True)
    inPkgs = MongoDB.ListField(MongoDB.IntField())
    outPkgs = MongoDB.ListField(MongoDB.IntField())
    inErrPkgs = MongoDB.ListField(MongoDB.IntField())
    outErrPkgs = MongoDB.ListField(MongoDB.IntField())
    time = MongoDB.ListField(MongoDB.DateTimeField())
    router = MongoDB.ReferenceField(Router, required=True, reverse_delete_rule=MongoDB.CASCADE)

    def to_json(self):
        return {
            'description': self.description,
            'status': self.status,
            'inPkgs': self.inPkgs,
            'outPkgs': self.outPkgs,
            'inErrPkgs': self.inErrPkgs,
            'outErrPkgs': self.outErrPkgs,
            'time': self.time,
            'router': self.router.to_json()
        }