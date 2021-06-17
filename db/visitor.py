import uuid

from psycopg2.extras import RealDictCursor
from db import db, Visitor


def add_visitor(vehicle_license) -> Visitor:
    cursor: RealDictCursor = db.cursor(cursor_factory=RealDictCursor)
    visitor_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO visitors VALUES({} = %s, {} = %s)"
                   .format("id", "license"),
                   [visitor_id, vehicle_license])
    cursor.close()
    return Visitor(visitor_id, vehicle_license)


def get_visitor_by_id(visitor_id) -> Visitor:
    cursor: RealDictCursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM visitors WHERE {} = %s"
                   .format("id"),
                   [visitor_id])
    response = cursor.fetchone()
    cursor.close()
    return Visitor.from_dict(response) if response else None


def get_visitor_by_vehicle_license(vehicle_license) -> Visitor:
    cursor: RealDictCursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM visitors WHERE {} = %s"
                   .format("license"),
                   [vehicle_license])
    response = cursor.fetchone()
    cursor.close()
    return Visitor.from_dict(response) if response else None
