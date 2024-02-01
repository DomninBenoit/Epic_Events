from authentication.model import Collaborateur, Departement, Role
from common.base import Session

# Initialiser une session SQLAlchemy
session = Session()

# Créer les rôles
role_commercial = Role(nom="commercial")
role_support = Role(nom="support")
role_gestion = Role(nom="gestion")

# Créer un nouveau collaborateur
nouveau_collaborateur = Collaborateur(
    nom_utilisateur='domnin',
    email='domnin@example.com',
    role_id=role_gestion.id
)

# Définir le mot de passe
nouveau_collaborateur.set_mot_de_passe('password123')

# Ajouter le collaborateur à la session et valider les changements
session.add(role_gestion)
session.add(role_commercial)
session.add(role_support)
session.add(nouveau_collaborateur)
session.commit()
