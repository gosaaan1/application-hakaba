from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from settings.environ import Environ

ENGINE = create_engine(Environ.database_uri, echo=Environ.db_trace)

session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
)

Base = declarative_base()