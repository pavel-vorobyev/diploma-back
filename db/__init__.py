import os

from sqlalchemy import create_engine, Column, String, ForeignKey, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, scoped_session

db_host = os.environ["DB_HOST"]
db_name = os.environ["DB_NAME"]
db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)
DbBase = declarative_base(metadata=metadata)

db_url = "postgresql://{}:{}@{}/{}".format(db_user, db_password, db_host, db_name)
engine = create_engine(db_url, convert_unicode=True)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DBSession = scoped_session(session)


class Guard(DbBase):
    __tablename__ = "guards"

    id = Column(String, primary_key=True)
    name = Column(String)
    login = Column(String)
    password = Column(String)

    accepted_visits = relationship("Visit")


class Visitor(DbBase):
    __tablename__ = "visitors"

    id = Column(String, primary_key=True)
    license = Column(String)


class Visit(DbBase):
    __tablename__ = "visits"

    id = Column(String, primary_key=True)
    guard_id = Column(String, ForeignKey("guards.id"))

    visitor_id = Column(String, ForeignKey("visitors.id"))
    visitor = relationship("Visitor", load_on_pending=True, foreign_keys=[visitor_id])


DbBase.metadata.create_all(engine)
