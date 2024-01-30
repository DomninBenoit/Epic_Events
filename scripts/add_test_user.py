from authentication.model import Collaborateur, Departement, Role
from common.base import Session

# Initialiser une session SQLAlchemy
session = Session()

# création role
role_gestionnaire = Role(
    nom="gestion"
)

Role(
    nom="commercial"
)

Role(
    nom="support"
)

# Créer un nouveau collaborateur
nouveau_collaborateur = Collaborateur(
    nom_utilisateur='domnin',
    email='domnin@example.com',
    role_id=role_gestionnaire.id
)

# Définir le mot de passe
nouveau_collaborateur.set_mot_de_passe('password123')

# Ajouter le collaborateur à la session et valider les changements
session.add(nouveau_collaborateur)
session.commit()
