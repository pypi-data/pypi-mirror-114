from datetime import datetime

from main.extension import db

from flask_restful_helper.utils import get_uuid


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), default=get_uuid, primary_key=True, nullable=False)
    username = db.Column(db.String(length=60), nullable=False)
    password = db.Column(db.String(length=60), nullable=False)
    email = db.Column(db.String(length=100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now)
