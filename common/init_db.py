from common.base import Base, engine
from client_management.model import Client
from authentication.model import Collaborateur, Role
from contract_management.model import Contrat
from events_management.model import Evenement


def init_db():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
