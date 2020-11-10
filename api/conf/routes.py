#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_restful import Api
# from flask_cors import cross_origin
from api.handlers.UserHandlers import (AddUser, DataAdminRequired,DataUserRequired, Login, Logout, RefreshToken, Register, ResetPassword,UsersData, UsersAllData, UserData)

from api.handlers.LanguageHandlers import (LanguagesAllData, LanguageData, LanguagePageData, LanguageTitle, LanguageDelete, LanguageStatus)

from api.handlers.CountryHandlers import (CountriesAllData, CountryData, CountryDelete)

# @cross_origin()
def generate_routes(app):

    # Create api.
    api = Api(app)

    # Add all routes resources.
    # Register page.
    api.add_resource(Register, '/v1/auth/register')

    # Login page.
    api.add_resource(Login, '/v1/auth/login')

    # Logout page.
    api.add_resource(Logout, '/v1/auth/logout')

    # Refresh page.
    api.add_resource(RefreshToken, '/v1/auth/refresh')

    # Password reset page. Not forgot.
    api.add_resource(ResetPassword, '/v1/auth/password_reset')

    # Get all users with admin permissions.
    api.add_resource(UsersAllData, '/v1/members/admin')

    # Get a user info with admin permissions.
    api.add_resource(UserData, '/v1/member/admin')

    # Get users page with admin permissions.
    api.add_resource(UsersData, '/users')

    # Example admin handler for admin permission.
    api.add_resource(DataAdminRequired, '/data_admin')

    # Example user handler for user permission.
    api.add_resource(DataUserRequired, '/data_user')

    # Example user handler for user permission.
    api.add_resource(AddUser, '/user_add')

    # Get all languages
    api.add_resource(LanguagesAllData, '/v1/langs/admin')
    # Get all language Details
    api.add_resource(LanguageData, '/v1/lang/admin')
    # Get page language Details
    api.add_resource(LanguagePageData, '/v1/langPage/admin')
    # Get language title
    api.add_resource(LanguageTitle, '/v1/langTitle/admin')
    # Delete language
    api.add_resource(LanguageDelete, '/v1/langDelete/admin')
    # Active language
    api.add_resource(LanguageStatus, '/v1/langActive/admin')
    
    # Get all countries
    api.add_resource(CountriesAllData, '/v1/countries/admin')
    # Get country
    api.add_resource(CountryData, '/v1/country/admin')
    # Delete country
    api.add_resource(CountryDelete, '/v1/countryDelete/admin')
