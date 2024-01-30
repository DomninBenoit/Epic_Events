from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from common.base import Base


class Evenement(Base):
    __tablename__ = 'evenements'
    id = Column(Integer, primary_key=True)
    contrat_id = Column(Integer, ForeignKey('contrats.id'))
    contact_support_id = Column(Integer, ForeignKey('collaborateurs.id'))
    date_debut = Column(DateTime)
    date_fin = Column(DateTime)
    lieu = Column(String(255))
    nombre_participants = Column(Integer)
    notes = Column(String)
