from flask import g
from sqlalchemy.sql import func
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
)
from sqlalchemy.ext.declarative import (
    as_declarative,
    declared_attr,
)
from sqlalchemy import (
    create_engine,
    exists,
    inspect,
    Integer,
    Column,
    Boolean,
    DateTime,
)

from app import config


@as_declarative()
class Model:
    id = Column(Integer, primary_key=True)
    deleted = Column(Boolean, default=False)
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now())

    @declared_attr
    def __tablename__(cls):
        s = cls.__name__.lower()
        return s

    @classmethod
    def _db_engine(cls):
        engine = create_engine(config.db)
        return engine

    @classmethod
    def reset(cls):
        pass

    @classmethod
    def setup(cls):
        engine = cls._db_engine()
        cls.metadata.create_all(engine)

    @classmethod
    def register_session(cls):
        engine = cls._db_engine()
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        g.db_session = Session

    @classmethod
    def remove_session(cls, response):
        if response.status_code == 500:
            g.db_session.rollback()
        else:
            g.db_session.remove()
        return response

    @classmethod
    def db_session(cls):
        s = g.db_session
        return s

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = (f'{k} = {v}' for k, v in self.__dict__.items())
        s = '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))
        return s

    @classmethod
    def all_attrs(cls):
        attrs = []
        columns = inspect(cls).mapper.column_attrs
        for c in columns:
            attrs.append(c.key)
        return attrs

    def dict(self):
        columns = inspect(self).mapper.column_attrs
        d = {c.key: getattr(self, c.key) for c in columns}
        return d

    @classmethod
    def new(cls, **conditions):
        m = cls()
        for name, value in conditions.items():
            setattr(m, name, value)
        s = cls.db_session()
        s.add(m)
        s.commit()
        return m

    @classmethod
    def delete(cls, model_id):
        cls.update(model_id, deleted=True)

    @classmethod
    def update(cls, model_id, **conditions):
        session = cls.db_session()
        m = session.query(cls).filter_by(id=model_id).first()
        for name, value in conditions.items():
            setattr(m, name, value)
        m.updated_time = func.now()
        session.add(m)
        session.commit()
        return m

    @classmethod
    def all(cls, **conditions):
        query = cls.db_session().query(cls)
        ms = query.filter_by(deleted=False, **conditions).all()
        return ms

    @classmethod
    def one(cls, **conditions):
        query = cls.db_session().query(cls)
        m = query.filter_by(deleted=False, **conditions).first()
        return m

    @classmethod
    def exist(cls, **conditions):
        e = exists()
        for name, value in conditions.items():
            e = e.where(getattr(cls, name) == value)
        session = cls.db_session()
        q = session.query(e)
        r = q.scalar()
        return r
