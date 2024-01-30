from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from common.base import Base


class Contrat(Base):
    __tablename__ = 'contrats'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    contact_commercial_id = Column(Integer, ForeignKey('collaborateurs.id'))
    montant_total = Column(Numeric(12, 2))
    montant_restant = Column(Numeric(12, 2))
    date_creation = Column(Date)
    statut = Column(String(100))