#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import json
from datetime import datetime

from flask import g, request
from flask_restful import Resource

import api.error.errors as error
from api.conf.auth import auth, refresh_jwt
from api.database.database import db
from api.models.models import Blacklist, User, Language, Country
from api.roles import role_required
from api.schemas.schemas import UserSchema
from flask import jsonify
# Auth
class Register(Resource):
    @staticmethod
    def post():
       
        try:
            # Get username, password and email.
            username, email, password, first_name, last_name, user_role, user_country, user_language = request.json.get('name').strip(), request.json.get('email').strip(), request.json.get('password').strip(),  request.json.get('firstName').strip(), request.json.get('lastName').strip(), request.json.get('role'), request.json.get('country'), request.json.get('language') 
        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Username, password or email is wrong. " + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        # Check if any field is none.
        if username is None or password is None or email is None:
            return error.INVALID_INPUT_422

        # Get user if it is existed.
        user = User.query.filter_by(email=email).first()

        # Check if user is existed.
        if user is not None:
            return error.ALREADY_EXIST

        # Create a new user.
        user = User(username=username, email=email, password=password, first_name=first_name, last_name= last_name, user_role = user_role, user_country = user_country, user_language = user_language)

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        # Return success if registration is completed.
        return {'status': 'Registration completed.'}


class Login(Resource):
    @staticmethod
    def post():

        try:
            # Get user email and password.
            email, password = request.json.get('email').strip(), request.json.get('password').strip()


        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Email or password is wrong. " + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        # Check if user information is none.
        if email is None or password is None:
            return error.INVALID_INPUT_422

        # Get user if it is existed.
        user = User.query.filter_by(email=email, password=password).first()

        # Check if user is not existed.
        if user is None:
            return error.DOES_NOT_EXIST
        # If user is admin.
        if user.user_role == 0:

            # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
            access_token = user.generate_auth_token(0)
        # If user is an individual.
        elif user.user_role == 1:

            # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 2, 1, 0.
            access_token = user.generate_auth_token(2)
        # If user is content provider.
        elif user.user_role == 2:

            # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
            access_token = user.generate_auth_token(1)
        # If user is content provider, but can be normal user too.
        elif user.user_role == 3:

            # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 2, 1, 0.
            access_token = user.generate_auth_token(3)
        else:
            return error.INVALID_INPUT_422

        # Generate refresh token.
        refresh_token = refresh_jwt.dumps({'email': email})

        # Return access token and refresh token.
        return {'status': 'Login success', 'username': user.username, 'user_role': user.user_role, 'access_token': access_token.decode(), 'refresh_token': refresh_token.decode()}


class Logout(Resource):
    @staticmethod
    @auth.login_required
    def post():

        # Get refresh token.
        refresh_token = request.json.get('refresh_token')

        # Get if the refresh token is in blacklist
        ref = Blacklist.query.filter_by(refresh_token=refresh_token).first()

        # Check refresh token is existed.
        if ref is not None:
            return {'status': 'already invalidated', 'refresh_token': refresh_token}

        # Create a blacklist refresh token.
        blacklist_refresh_token = Blacklist(refresh_token=refresh_token)

        # Add refresh token to session.
        db.session.add(blacklist_refresh_token)

        # Commit session.
        db.session.commit()

        # Return status of refresh token.
        return {'status': 'invalidated', 'refresh_token': refresh_token}


class RefreshToken(Resource):
    @staticmethod
    def post():

        # Get refresh token.
        refresh_token = request.json.get('refresh_token')

        # Get if the refresh token is in blacklist.
        ref = Blacklist.query.filter_by(refresh_token=refresh_token).first()

        # Check refresh token is existed.
        if ref is not None:

            # Return invalidated token.
            return {'status': 'invalidated'}

        try:
            # Generate new token.
            data = refresh_jwt.loads(refresh_token)

        except Exception as why:
            # Log the error.
            logging.error(why)

            # If it does not generated return false.
            return False

        # Create user not to add db. For generating token.
        user = User(email=data['email'])

        # New token generate.
        token = user.generate_auth_token(False)

        # Return new access token.
        return {'access_token': token}


class ResetPassword(Resource):
    @auth.login_required
    def post(self):

        # Get old and new passwords.
        old_pass, new_pass = request.json.get('old_pass'), request.json.get('new_pass')

        # Get user. g.user generates email address cause we put email address to g.user in models.py.
        user = User.query.filter_by(email=g.user).first()

        # Check if user password does not match with old password.
        if user.password != old_pass:

            # Return does not match status.
            return {'status': 'old password does not match.'}

        # Update password.
        user.password = new_pass

        # Commit session.
        db.session.commit()

        # Return success status.
        return {'status': 'password changed.'}

# Users
class UsersAllData(Resource):
    # @auth.login_required
    # @role_required.permission(2)
    def get(self):
        try:
            # users = User.query.all()
            users = User.query.join(Language, User.user_language == Language.id).join(Country, User.user_country == Country.id).add_columns(User.id, User.first_name, User.last_name, User.email, User.user_role, Language.name.label('language'), Country.name.label('country')).all()
            
            # Create user schema for serializing.
            user_schema = UserSchema(many=True)

            # Get json data
            data = user_schema.dump(users)

            # Return json data from db.
            return data

        except Exception as why:

            # Log the error.
            logging.error(why)

            # Return error.
            return error.INVALID_INPUT_422

# auth.login_required: Auth is necessary for this handler.
# role_required.permission: Role required user=0, admin=1 and super admin=2.

class UsersData(Resource):
    @auth.login_required
    @role_required.permission(2)
    def get(self):
        try:

            # Get usernames.
            usernames = [] if request.args.get('usernames') is None else request.args.get('usernames').split(',')

            # Get emails.
            emails = [] if request.args.get('emails') is None else request.args.get('emails').split(',')

            # Get start date.
            start_date = datetime.strptime(request.args.get('start_date'), '%d.%m.%Y')

            # Get end date.
            end_date = datetime.strptime(request.args.get('end_date'), '%d.%m.%Y')


            # Filter users by usernames, emails and range of date.
            users = User.query\
                .filter(User.username.in_(usernames))\
                .filter(User.email.in_(emails))\
                .filter(User.created.between(start_date, end_date))\
                .all()

            # Create user schema for serializing.
            user_schema = UserSchema(many=True)

            # Get json data
            data, errors = user_schema.dump(users)

            # Return json data from db.
            return data

        except Exception as why:

            # Log the error.
            logging.error(why)

            # Return error.
            return error.INVALID_INPUT_422

# auth.login_required: Auth is necessary for this handler.
# role_required.permission: Role required user=0, admin=1 and super admin=2.

class UserData(Resource):
    # @auth.login_required
    # @role_required.permission(2)
    def get(self):
        try:
            # Get user id
            userid = request.args.get('id')
            users = User.query.filter_by(id=userid).join(Language, User.user_language == Language.id).join(Country, User.user_country == Country.id).add_columns(User.id, User.first_name, User.last_name, User.email, User.user_role, Language.name.label('language'), Country.name.label('country')).all()

            # Create user schema for serializing.
            user_schema = UserSchema(many=True)
            # Get json data
            data = user_schema.dump(users)
            # Return json data from db.
            return data

        except Exception as why:
            # Log the error.
            logging.error(why)
            # Return error.
            return error.INVALID_INPUT_422

# auth.login_required: Auth is necessary for this handler.
# role_required.permission: Role required user=0, admin=1 and super admin=2.

class DataAdminRequired(Resource):
    @auth.login_required
    @role_required.permission(1)
    def get(self):

        return "Test admin data OK."


class AddUser(Resource):
    @auth.login_required
    @role_required.permission(2)
    def get(self):

        return "OK"


class DataUserRequired(Resource):

    @auth.login_required
    def get(self):

        return "Test user data OK."
