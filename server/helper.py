import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from passlib.hash import sha256_crypt
from flask_restful import reqparse
from functools import wraps
from flask import request, jsonify
from models import models
from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt_claims,
    get_jwt_identity
)


def pw_encrypt(pw):
    return sha256_crypt.hash(pw)


def verify_pw(pw_str, pw_hash):
    return sha256_crypt.verify(pw_str, pw_hash)


def verify_signup_input(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
        parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
        parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")
        parser.parse_args()

        return f(*args, **kwargs)
    return decorated


def get_role_id(role='regular'):
    role = models.Role.query.filter_by(name=role).first()
    return role.id

def get_request_type_id(type='pending'):
    request_type = models.Request_Type.query.filter_by(name=type).first()
    return request_type.id


def validate_request(*expected_args):
    def validate_input(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not request.json:
                return {
                    'status': 'fail',
                    "data": {"message": "Request must be a valid JSON"}
                }, 400

            payload = request.get_json()
            if payload:
                for value in expected_args:
                    if value == 'status' and value not in payload: continue
                    if value not in payload or not payload[value]:
                        return {
                            "status": "fail",
                            "data": {"message": value + " is required"}
                        }, 400
                    if type(payload[value]) != str or not payload[value].strip(' '):
                        return {
                            "status": "fail",
                            "data": {"message": value + " must contain valid strings"}
                        }, 400
            return f(*args, **kwargs)
        return decorated
    return validate_input


# Here is a custom decorator that verifies the JWT is present in
# the request, as well as insuring that this user has a role of
# `admin` in the access token
def admin_required(fn):
    @wraps(fn)
    def authenticated(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] != 'admin':
            return jsonify(dict(
                status="fail",
                messsage="Access Denied!"
            )), 401
        return fn(*args, **kwargs)
    return authenticated


def validate_user_update_request(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        current_user = get_jwt_identity()
        request_id = request.url.rstrip('/').split('/')[-1]
        user_request = models.Request.query.get(request_id)

        if not user_request:
            return {
                "status": "fail",
                "message": "Request not found!"
            }, 404

        if current_user['id'] != str(user_request.owner_id):
            return {
                "status": "fail",
                "message": "Request denied!"
            }, 403

        if user_request.status in ['approved', 'disapproved', 'resolved']:
            return {
                "status": "fail",
                "message": "Request cannot be edited!"
            }, 403

        return fn(*args, **kwargs)
    return decorated
