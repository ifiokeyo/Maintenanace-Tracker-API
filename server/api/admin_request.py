from flask import request, jsonify
from flask_restful import Resource
from models import models
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper import get_role_id, admin_required

Request = models.Request


class AdminRequestResource(Resource):
    @jwt_required
    @admin_required
    def get(self):
        all_requests = Request.query.all()
        if not all_requests:
            return {
                "status": "success",
                "data": {
                    "requests": [],
                    "message": "There are no requests!"
                }
            }, 200

        requests = [user_request.serialize() for user_request in all_requests]
        response = jsonify(dict(
            status="success",
            data={
                "requests": requests
            }
        ))
        response.status_code = 200
        return response


    @jwt_required
    @admin_required
    def put(self, request_id):
        status = request.url.rstrip('/').split('/')[-1]
        user_request = Request.query.get(request_id)
        if not user_request:
            return {
                "status": "fail",
                "message": "Request not found!"
            }, 404

        if user_request.status == '{}d'.format(status):
            return {
                "status": "fail",
                "message": "Request has been {}d already!".format(status)
            },400

        user_request.status = '{}d'.format(status)
        user_request.save()
        updated_request = user_request.serialize()

        response = jsonify(dict(
            status="success",
            data={
                "message": "Request {}d!".format(status),
                "request": updated_request
            }
        ))
        response.status_code = 200
        return response

