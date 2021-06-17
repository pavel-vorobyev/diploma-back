import json

import psycopg2

# db_host = os.environ["DB_HOST"]
# db_name = os.environ["DB_NAME"]
# db_user = os.environ["DB_USER"]
# db_password = os.environ["DB_PASSWORD"]

db_host = "localhost"
db_name = "diploma"
db_user = "diploma"
db_password = "qwerty"


def get_db():
    l_db = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'"
                            .format(db_name, db_user, db_host, db_password))
    l_db.autocommit = True
    return l_db


db = get_db()


class JsonableModel:

    def to_dict(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, sort_keys=False))


class Guard(JsonableModel):
    id: str
    name: str
    login: str
    password: str

    def __init__(self, o_id, name, login, password):
        self.id = o_id
        self.name = name
        self.login = login
        self.password = password

    @staticmethod
    def from_dict(d):
        return Guard(d["id"], d["name"], d["login"], d["password"])


class Visitor(JsonableModel):
    id: str
    license: str

    def __init__(self, o_id, o_license):
        self.id = o_id
        self.license = o_license

    @staticmethod
    def from_dict(d):
        return Visitor(d["id"], d["license"])


class Visit(JsonableModel):
    id: str
    guard_id: str
    date: str
    is_allowed: bool
    scan_file: str
    visitor_id: str
    visitor: Visitor

    def __init__(self, o_id, guard_id, date, is_allowed, scan_file, visitor_id):
        self.id = o_id
        self.guard_id = guard_id
        self.date = date
        self.is_allowed = is_allowed
        self.scan_file = scan_file
        self.visitor_id = visitor_id

    @staticmethod
    def from_dict(d):
        return Visit(d["id"], d["guard_id"], d["date"], d["is_allowed"], d["scan_file"], d["visitor_id"])
