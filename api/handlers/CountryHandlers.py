import logging
import json
from datetime import datetime

from flask import g, request
from flask_restful import Resource

import api.error.errors as error
from api.conf.auth import auth, refresh_jwt
from api.database.database import db
from api.models.models import Country
from flask import jsonify
from api.schemas.schemas import CountrySchema

class CountryData(Resource):
    # @auth.login_required
    # @role_required.permission(2)
    
    def post(self):
        # print('detail print')
        try:
            # get data
            id, name, currency, fx, land_register, right_of_lien, solvency, abstract_lr, valuation_fee, solvency_rate, reference_1, reference_2, stamp_duty, country_costs = request.json.get('id'), request.json.get('name'), request.json.get('currency'), request.json.get('fx'), request.json.get('land_register'), request.json.get('right_of_lien'), request.json.get('solvency'), request.json.get('abstract_lr'), request.json.get('valuation_fee'), request.json.get('solvency_rate'), request.json.get('reference_1'), request.json.get('reference_2'), request.json.get('stamp_duty'), request.json.get('country_costs')
            print('country is')
            print(id)
        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("data wrong. " + str(why))
            # Return invalid input error.
            return error.INVALID_INPUT_422
        # check if the same country is existed
        data = Country.query.filter(Country.id != id, Country.name == name).first()
        print(data)
        if data is not None:
            return error.ALREADY_EXIST
        else:
            # check if data is existed
            data = Country.query.filter_by(id=id).first()
            # if data is existed.
            if data is not None:
                # return error.ALREADY_EXIST
                data.name = name
                data.currency = currency
                data.fx = fx
                data.land_register = land_register
                data.right_of_lien = right_of_lien
                data.solvency = solvency
                data.abstract_lr = abstract_lr
                data.valuation_fee = valuation_fee
                data.solvency_rate = solvency_rate
                data.reference_1 = reference_1
                data.reference_2 = reference_2
                data.stamp_duty = stamp_duty
                data.country_costs = country_costs
                db.session.commit()
                # Return success if update is completed.
                return {'status': 'Updated Successfully!'}
            else:
                # Create a new data.
                data = Country(name=name, currency=currency, fx=fx, land_register=land_register, right_of_lien=right_of_lien, solvency=solvency, abstract_lr=abstract_lr, valuation_fee=valuation_fee, solvency_rate=solvency_rate, reference_1=reference_1, reference_2=reference_2, stamp_duty=stamp_duty, country_costs=country_costs)
                # Add user to session.
                db.session.add(data)
                # Commit session.
                db.session.commit()

                # Return success if creation is completed.
                return {'status': 'Created Successfully!'}

class CountryDelete(Resource):
    # @auth.login_required
    # @role_required.permission(2)
    def get(self):
        try:
            id = request.args.get('id')
            print(id)
            country = Country.query.filter_by(id=id).first()
            # # Add user to session.
            db.session.delete(country)
            # Commit session.
            db.session.commit()

            return {'status': 'Deleted!'}

        except Exception as why:

            # Log the error.
            logging.error(why)

            # Return error.
            return error.INVALID_INPUT_422

# Countries
class CountriesAllData(Resource):
    # @auth.login_required
    # @role_required.permission(2)
    def get(self):
        try:
            countries = Country.query.all()
            
            # Create user schema for serializing.
            country_schema = CountrySchema(many=True)

            # Get json data
            data = country_schema.dump(countries)
            # Return json data from db.
            return data

        except Exception as why:

            # Log the error.
            logging.error(why)

            # Return error.
            return error.INVALID_INPUT_422

