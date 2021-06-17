import uuid

from psycopg2.extras import RealDictCursor

from db import db, Guard


def add(guard_name, guard_login, guard_password) -> Guard:
    cursor: RealDictCursor = db.cursor(cursor_factory=RealDictCursor)
    guard_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO guards VALUES(%s, %s, %s, %s)",
                   [guard_id, guard_name, guard_login, guard_password])
    cursor.close()
    return Guard(guard_id, guard_name, guard_login, guard_password)


def login(guard_login, guard_password) -> Guard:
    cursor: RealDictCursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM guards WHERE {} = %s AND {} = %s"
                   .format("login", "password"),
                   [guard_login, guard_password])
    response = cursor.fetchone()
    cursor.close()
    return Guard.from_dict(response) if response else None
