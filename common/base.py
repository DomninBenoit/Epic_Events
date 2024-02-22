from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///epic_events_crm.db')
Base = declarative_base()

# Initialiser une session SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()