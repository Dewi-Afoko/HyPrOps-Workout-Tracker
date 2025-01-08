from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from lib.utilities.helper_functions import get_credentials, find_user_from_jwt
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from lib.utilities.helper_functions import get_credentials, find_user_from_jwt, check_for_error
from mongoengine import NotUniqueError, ValidationError
from models import User
from routes.restx_models.user_models import user_get_failure, user_get_success, user_ns, user_registration_error, user_registration_request, user_registration_success, user_update_failure, user_update_request, user_update_success, user_details_success, user_details_error


@user_ns.route('/register')
class UserRegister(Resource):
    @user_ns.expect(user_registration_request)
    @user_ns.doc(responses={
        201: ('Created', user_registration_success),
        400: ('Bad Request', user_registration_error),
        409: ('Conflict', user_registration_error),
    })
    def post(self):
        data = request.get_json()

        credentials, status_code = get_credentials(data)
        if status_code == 400:
            return credentials, status_code

        try:
            user = User(username=credentials['username'], password=credentials['password'])
            user.hash_password()
            user.save()
            return {'message': f'{user.username} successfully registered!'}, 201
        except NotUniqueError:
            return {'error': 'Username unavailable'}, 409
        

@user_ns.route('/list')
class UserGet(Resource):
    @user_ns.doc(responses={
        200: ('Success', user_get_success),
        404: ('Not Found', user_get_failure),
    })
    @jwt_required()
    def get(self):
        user_list = [user.to_dict() for user in User.objects()]
        if not user_list:
            return {'error': 'No users found!'}, 404
        return {'message': user_list}, 200
    
@user_ns.route('/details')
class UserDetails(Resource):
    @user_ns.doc(responses={
        200: ('Success', user_details_success),
        404: ('Not Found', user_details_error),
    })
    @jwt_required()
    def get(self):
        user = find_user_from_jwt()
        if check_for_error(user):
            return user
        
        return user.to_dict(), 200




@user_ns.route('/update_personal_data')
class UpdatePersonalData(Resource):
    @user_ns.expect(user_update_request)
    @user_ns.doc(responses={
        201: ('Created', user_update_success),
        400: ('Bad Request', user_update_failure),
    })
    @jwt_required()
    def patch(self):
        data = request.get_json()
        user = find_user_from_jwt()

        try:
            user.update_personal_details(**data)
            user.save()
            return {'message': 'Personal data updated'}, 201
        except ValidationError:
            return {'error': 'Failed to create Personal Data'}, 400
