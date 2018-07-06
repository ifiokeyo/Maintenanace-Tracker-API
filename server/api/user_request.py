from flask_restful import Resource
from flask import request, jsonify
from models import models
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper import (
    validate_request, get_role_id,
    get_request_type_id, validate_user_update_request
)


Request = models.Request
Request_Type = models.Request_Type


class UserRequestResource(Resource):
    @jwt_required
    @validate_request('description', 'type')
    def post(self):
        current_user = get_jwt_identity()
        payload = request.get_json()
        request_type = Request_Type.query.filter_by(name=payload['type']).first()
        if request_type:
            request_type_id = request_type.id
        else:
            new_request_type = Request_Type(name=payload['type'])
            new_request_type.save()
            request_type_id = new_request_type.id

        new_request = Request(
            description=payload['description'],
            type_id=request_type_id,
            owner_id=current_user['id']
        )
        new_request.save()
        _request = new_request.serialize()

        response = jsonify(dict(
            status='success',
            data={
                "request": _request,
                "message": 'Request was created succesfully waiting approval'
            }
        ))
        response.status_code = 201
        return response


    @jwt_required
    def get(self, request_id=None):
        current_user = get_jwt_identity()
        if request_id:
            user_request = Request.query.filter_by(id=request_id, owner_id=current_user['id']).first()

            if not user_request:
                return {
                    "status": "fail",
                    "data": {
                        "message": "Request not found"
                    }
                }, 404

            _request = user_request.serialize()

            response = jsonify(dict(
                status="success",
                data={
                    "request": _request
                }
            ))
            response.status_code = 200
            return response

        user_requests = Request.query.filter_by(owner_id=current_user['id']).all()
        if not user_requests:
            return {
                "status": "success",
                "data": {
                    "requests": [],
                    "message": "You do not have any request!"
                }
            }, 200
        requests = [user_request.serialize() for user_request in user_requests]
        response = jsonify(dict(
            status="success",
            data={
                "requests": requests
            }
        ))
        response.status_code = 200
        return response


    @jwt_required
    @validate_request('description', 'type')
    @validate_user_update_request
    def put(self, request_id):
        current_user = get_jwt_identity()
        payload = request.get_json()
        request_type_id = get_request_type_id(payload['type'])

        user_request = Request.query.get(request_id)

        user_request.description = payload['description']
        user_request.type_id = request_type_id

        user_request.save()

        updated_request = user_request.serialize()

        response = jsonify(dict(
            status="success",
            data={
                "request": updated_request,
                "message": "Request updated successfully!"
            }
        ))
        response.status_code = 200
        return response


