from inflection import tableize
from sqlalchemy import DateTime
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql import expression


class CustomBase(object):
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls):
        return tableize(cls.__name__)


Base = declarative_base(cls=CustomBase)


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"