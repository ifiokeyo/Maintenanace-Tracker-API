import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask_restful import Resource
from flask import request, jsonify
from models import models
from helper import validate_request
from flask_jwt_extended import jwt_required, get_jwt_identity

Role = models.Role


class RoleResource(Resource):

    @validate_request('name')
    def post(self):
        payload = Role.parser.parse_args()
        role = Role.query.filter_by(name=payload['name']).first()
        if role:
            return {
                'status': 'fail',
                'message': '{} role already exists'.format(role.name)
            }, 403

        new_role = Role(
            name=payload['name']
        )
        new_role.save()
        _role = new_role.serialize()

        response = jsonify(dict(
            status='success',
            data={
                'role': _role,
                'message': 'Role created successfully'
            }
        ))
        response.status_code=201
        return response


    @jwt_required
    def get(self):
        roles = Role.query.all()
        if not roles:
            return {
                'status': 'success',
                'data': {
                    'roles': [],
                    'message': 'No Roles'
                }
            }, 200

        _roles = [role.serialize() for role in roles]

        response = jsonify(dict(
            status='success',
            data={
                'roles': _roles
            },
            statusCode=200
        ))
        return response
