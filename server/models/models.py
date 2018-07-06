import json
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from helper import get_role_id
from flask_restful import reqparse


db = SQLAlchemy()


class ModelOpsMixin(object):
    """
    Contains the serialize method to convert objects to a dictionary
    """

    def serialize(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns if column.name != 'password'}

    def save(self):
        db.session.add(self)
        db.session.commit()


class Request_Type(db.Model, ModelOpsMixin):
    __tablename__ = "Request_type"

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = db.Column(db.String(40), nullable=False)

    requests = db.relationship("Request", backref="Request_Type", lazy='dynamic')

    def __repr__(self):
        return '<Request_Type %r>' % self.name


class Request(db.Model, ModelOpsMixin):
    __tablename__ = "Request"

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, default="pending", nullable=False)  # status can be either of the fllg: pending, ongoing, approved, rejected, done
    type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Request_type.id'), nullable=False)
    owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey('User.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    type = db.relationship("Request_Type", backref="Request", lazy=True)


    def __repr__(self):
        return '<Request %r>' % self.description


class User(db.Model, ModelOpsMixin):
    __tablename__ = "User"

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(), nullable=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Role.id'), nullable=False, default=get_role_id)

    def __repr__(self):
        return '<User %r>' % self.name


class Role(db.Model, ModelOpsMixin):
    __tablename__ = "Role"

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Name cannot be empty")

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)


    def __repr__(self):
        return '<Role %r>' % self.name


class RevokedAccessToken(db.Model, ModelOpsMixin):
    __tablename__ = "Revoked_token"

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    jti = db.Column(db.String(), nullable=False)

    @classmethod
    def is_token_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)

