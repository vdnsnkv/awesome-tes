from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from user_service.config import config

engine = create_engine(
    config.db_connstring,
    convert_unicode=True,
    echo=False,
)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session: Session = scoped_session(session_factory)

Base = declarative_base()
Base.query = db_session.query_property()


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(metadata=Base.metadata)
migrate = Migrate()
