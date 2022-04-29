from flask import Blueprint, cli
from flask_sqlalchemy import SQLAlchemy
from app import config
import os
db = SQLAlchemy()

database = Blueprint('database', __name__,)

@database.cli.command('create')
def init_db():
    db.create_all()

def get_db():
    return db
