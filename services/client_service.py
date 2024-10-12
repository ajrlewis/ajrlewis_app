from app import db
from models import Client


def get_all() -> list[Client]:
    clients = db.session.query(Client).order_by(Client.name).all()
    return clients
