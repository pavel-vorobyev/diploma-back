import uuid

from psycopg2.extras import RealDictCursor

from db import db, Visit
from db.visitor import get_visitor_by_id


def add_visit(guard_id, visitor_id, date, is_allowed, scan_file) -> Visit:
    cursor: RealDictCursor = db.cursor(cursor_factory=RealDictCursor)
    visit_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO visits VALUES(%s, %s, %s, %s, %s, %s)",
                   [visit_id, guard_id, date, visitor_id, scan_file, is_allowed])
    cursor.close()
    return Visit(visit_id, guard_id, date, is_allowed, scan_file, visitor_id)


def get_visits(guard_id):
    cursor: RealDictCursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM visits WHERE {} = %s ORDER BY {} DESC"
                   .format("guard_id", "date"),
                   [guard_id])
    response = cursor.fetchall()
    cursor.close()

    visits = [Visit.from_dict(item) for item in response]

    for visit in visits:
        visit.visitor = get_visitor_by_id(visit.visitor_id)

    return visits
