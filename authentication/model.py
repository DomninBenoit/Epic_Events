import enum
import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from common.base import Base


class Departement(enum.Enum):
    commercial = "commercial"
    support = "support"
    gestion = "gestion"


class Collaborateur(Base):
    __tablename__ = 'collaborateurs'
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    nom_utilisateur = Column(String(255), unique=True)
    mot_de_passe = Column(String(255))
    email = Column(String(255), unique=True)

    def set_mot_de_passe(self, password):
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.mot_de_passe = password_hash.decode('utf-8')


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    nom = Column(Enum(Departement))
