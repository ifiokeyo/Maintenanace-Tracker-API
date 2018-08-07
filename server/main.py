import os
from os.path import split, abspath
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import timedelta
from flask_jwt_extended import JWTManager


dotenv_path = split(abspath(__file__))[0].replace('server', '.env')
load_dotenv(dotenv_path)


try:
    from config import app_configuration
    from api.role import RoleResource
    from api.admin_request import AdminRequestResource
    from api.user_request import UserRequestResource
    from api.auth import LoginResource, SignupResource, LogoutResource
except ModuleNotFoundError:
    from server.config import app_configuration
    from server.api.role import RoleResource
    from server.api.admin_request import AdminRequestResource
    from server.api.user_request import UserRequestResource
    from server.api.auth import LoginResource, SignupResource, LogoutResource


def create_flask_app(environment):
    # initialize Flask
    app = Flask(__name__, instance_relative_config=True, static_folder=None)
    # to allow cross origin resource sharing
    CORS(app)
    app.config.from_object(app_configuration[environment])

    # initialize SQLAlchemy
    try:
        from models import models
    except ModuleNotFoundError:
        from server.models import models


    models.db.init_app(app)
    migrate = Migrate(app, models.db)
    app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=int(os.environ.get('ACCESS_TOKEN_LIFECYCLE')))
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    app.url_map.strict_slashes = False
    jwt = JWTManager(app)

    # test route
    @app.route('/')
    def index():
        return "Welcome to Maintenance Tracker"


    # Create a function that will be called whenever create_access_token
    # is used. It will take whatever object is passed into the
    # create_access_token method, and lets us define what custom claims
    # should be added to the access token.
    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        role = models.Role.query.get(str(user['role_id']))
        return {'role': role.name}

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return models.RevokedAccessToken.is_token_blacklisted(jti)

    # create endpoints
    api = Api(app, prefix='/api/v1')

    api.add_resource(
        LoginResource,
        '/auth/login',
        endpoint='login')

    api.add_resource(
        SignupResource,
        '/auth/signup',
        endpoint='signup')

    api.add_resource(
        LogoutResource,
        '/auth/logout',
        endpoint='logout'
    )

    api.add_resource(
        RoleResource,
        '/roles',
        endpoint='role')

    api.add_resource(
        UserRequestResource,
        '/users/requests',
        endpoint='user_requests')

    api.add_resource(
        AdminRequestResource,
        '/requests',
        endpoint="all_requests"
    )

    api.add_resource(
        AdminRequestResource,
        '/requests/<string:request_id>/approve',
        endpoint="approve_request"
    )

    api.add_resource(
        AdminRequestResource,
        '/requests/<string:request_id>/disapprove',
        endpoint="disapprove_request"
    )

    api.add_resource(
        AdminRequestResource,
        '/requests/<string:request_id>/resolve',
        endpoint="resolve_request"
    )

    api.add_resource(
        UserRequestResource,
        '/users/requests/<string:request_id>',
        endpoint="single_request"
    )


    # handle default 404 exceptions with a custom response
    @app.errorhandler(404)
    def resource_not_found(error):
        response = jsonify(dict(status=404, error='Not found', message='The '
                                'requested URL was not found on the server. If'
                                ' you entered the URL manually please check '
                                'your spelling and try again'))
        response.status_code = 404
        return response

    # handle default 500 exceptions with a custom response
    @app.errorhandler(500)
    def internal_server_error(error):
        response = jsonify(dict(status=500, error='Internal server error',
                                message="It is not you. It is me. The server "
                                "encountered an internal error and was unable "
                                "to complete your request.  Either the server "
                                "is overloaded or there is an error in the "
                                "application"))
        response.status_code = 500
        return response

    return app


if __name__ == "__main__":
    environment = os.getenv("FLASK_CONFIG")
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    app = create_flask_app(environment)
    app.run(port=9000)



