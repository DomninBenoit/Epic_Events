from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from common.base import Base


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    contact_commercial_id = Column(Integer, ForeignKey('collaborateurs.id'))
    nom_complet = Column(String(255))
    email = Column(String(255), unique=True)
    telephone = Column(String(20))
    nom_entreprise = Column(String(255))
    date_creation = Column(Date)
    derniere_update = Column(DateTime)

