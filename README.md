# Epic Events

Epic Events est une application de gestion de la relation client (CRM) conçue pour améliorer l'organisation et la gestion des événements, 
des clients, des contrats, et des interactions au sein de l'entreprise Epic Events.

## Fonctionnalités Principales

- Gestion des clients : Création, mise à jour, et suppression des clients.
- Gestion des contrats : Création, mise à jour, et suppression des contrats liés aux clients.
- Gestion des événements : Création, mise à jour, et suppression des événements organisés pour les clients.
- Gestion des collaborateurs : Gestion des accès et des rôles des collaborateurs de l'entreprise.
- Filtrage des contrats et des événements : Vue filtrée des contrats et des événements selon différents critères.

## Prérequis

- Python 3.9 ou supérieur
- SQLAlchemy pour l'ORM
- SQLite pour la base de données

## Installation

1. Cloner le dépôt Git :
    ```
    git clone https://github.com/DomninBenoit/Epic_Events.git
    ```
2. Se déplacer dans le répertoire du projet :
    ```
    cd Epic-Events
    ```
3. Créer un environnement virtuel Python :
    ```
    python -m venv venv
    ```
4. Activer l'environnement virtuel :
    - Sous Windows :
        ```
        .\venv\Scripts\activate
        ```
    - Sous Unix ou MacOS :
        ```
        source venv/bin/activate
        ```
5. Installer les dépendances :
    ```
    pip install -r requirements.txt
    ```

## Initialisation du Projet

1. Initialiser la base de données :
    ```
    python -m common.init_db
    ```
2. Ajouter un utilisateur gestion pour commencer à utiliser l'appli.
    ```
   python -m scripts.add_gestion_user
   ```

## Lancement de l'Application

Pour lancer l'application, exécutez :
```
python app.py
```
## Structure du Projet

- `authentication/` : Gestion de l'authentification et des utilisateurs.
- `client_management/` : Gestion des clients.
- `contract_management/` : Gestion des contrats.
- `events_management/` : Gestion des événements.
- `common/` : Contient les configurations communes, comme la connexion à la base de données.
- `app.py` : Point d'entrée de l'application.

## Journalisation des Erreurs avec Sentry

Le projet intègre Sentry pour la journalisation des erreurs. Sentry aide à surveiller et à résoudre les problèmes dans l'application en temps réel. La configuration de Sentry est incluse dans `app.py`. Assurez-vous d'ajouter votre propre DSN Sentry dans la configuration pour commencer à capturer les erreurs.

## Licence

[MIT](LICENSE)