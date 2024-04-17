#!/usr/bin/env bash

python -c '''
import sys

sys.path.append("./")

from app import create_app, db
from configs.prod_config import ProdConfig
from models.user import User
from models.client import Client
from models.invoice import Invoice

app = create_app(ProdConfig)
with app.app_context():
    db.create_all()
    db.session.commit()
'''
