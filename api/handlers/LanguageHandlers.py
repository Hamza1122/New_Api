import logging
import json
from datetime import datetime

from flask import g, request
from flask_restful import Resource

import api.error.errors as error
from api.conf.auth import auth, refresh_jwt
from api.database.database import db
from api.models.models import Language, LanguageDetail
from api.schemas.schemas import LanguageSchema
from api.schemas.schemas import LanguageDetailSchema
from flask import jsonify


# Languages
class LanguagesAllData(Resource):
    # @auth.login_required
    # @role_required.permission(2)
    def get(self):
        try:
            languages = Language.query.all()
            
            # Create user schema for serializing.
            language_schema = LanguageSchema(many=True)

            # Get json data
            data = language_schema.dump(languages)
            # Return json data from db.
            return data

        except Exception as why:

            # Log the error.
            logging.error(why)

            # Return error.
            return error.INVALID_INPUT_422

class LanguageData(Resource):
    # @auth.login_required
    # @role_required.permission(2)
    def get(self):
        try:
            lang_id = request.args.get('id')
            lang = LanguageDetail.query.filter_by(lang_id=lang_id).all()
            # Create schema for serializing.
            lang_schema = LanguageDetailSchema(many=True)
            # Get json data
            data = lang_schema.dump(lang)

            # Return json data from db.
            return data

        except Exception as why:

            # Log the error.
            logging.error(why)

            # Return error.
            return error.INVALID_INPUT_422
    
    def post(self):
        # print('detail print')
        try:
            # get data
            page_id, lang_id, content, translate = request.json.get('page_id'), request.json.get('lang_id'), request.json.get('content'), request.json.get('translate')
            # print('page_id is')
            # print(page_id)
        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("data wrong. " + str(why))
            # Return invalid input error.
            return error.INVALID_INPUT_422
        # check if data is existed
        data = LanguageDetail.query.filter_by(page_id=page_id, lang_id=lang_id, content=content).first()
        # if data is existed.
        if data is not None:
            # return error.ALREADY_EXIST
            data.translate = translate
            db.session.commit()
            # Return success if update is completed.
            return {'status': 'Updated Successfully!'}
        else:
            # Create a new data.
            data = LanguageDetail(page_id=page_id, lang_id=lang_id, content=content, translate=translate)
            # Add user to session.
            db.session.add(data)
            # Commit session.
            db.session.commit()

            # Return success if creation is completed.
            return {'status': 'Created Successfully!'}

class LanguagePageData(Resource):
    # @auth.login_required
    # @role_required.permission(2)
    def get(self):
        try:
            lang_id = request.args.get('lang_id')
            page_id = request.args.get('page_id')
            lang = LanguageDetail.query.filter_by(lang_id=lang_id, page_id=page_id).all()
            # Create schema for serializing.
            lang_schema = LanguageDetailSchema(many=True)
            # Get json data
            data = lang_schema.dump(lang)

            # Return json data from db.
            return data

        except Exception as why:

            # Log the error.
            logging.error(why)

            # Return error.
            return error.INVALID_INPUT_422

class LanguageTitle(Resource):
    # @auth.login_required
    # @role_required.permission(2)
    def get(self):
        try:
            lang_id = request.args.get('id')
            languages = Language.query.filter_by(id=lang_id).all()
            
            # Create user schema for serializing.
            language_schema = LanguageSchema(many=True)

            # Get json data
            data = language_schema.dump(languages)
            # Return json data from db.
            return data

        except Exception as why:

            # Log the error.
            logging.error(why)

            # Return error.
            return error.INVALID_INPUT_422
    def post(self):
        try:
            # get data
            id, name, foreign, status, lang_id = request.json.get('id'), request.json.get('name'), request.json.get('foreign'), request.json.get('status'), request.json.get('id')
            # print('name is')
            # print(lang_id)
        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("data wrong. " + str(why))
            # Return invalid input error.
            return error.INVALID_INPUT_422
        # check if the same language is existed
        data = Language.query.filter(Language.id != lang_id, Language.name == name).first()
        print(data)
        if data is not None:
            return error.ALREADY_EXIST_LANGUAGE
        else:
            # check if data is existed
            data = Language.query.filter_by(id=id).first()
            if data is not None:
                # return error.ALREADY_EXIST
                data.name = name
                data.foreign = foreign
                data.status = status
                db.session.commit()
                return {'status': 'Updated Successfully!'}
            else:
                # Create a new data.
                data = Language(name=name, foreign=foreign, status=status)
                # Add user to session.
                db.session.add(data)
                # Commit session.
                db.session.commit()

                # Return success if creation is completed.
                return {'status': 'Created successfully!'}

class LanguageDelete(Resource):
    # @auth.login_required
    # @role_required.permission(2)
    def get(self):
        try:
            lang_id = request.args.get('id')
            print(lang_id)
            lang_details = LanguageDetail.query.filter_by(lang_id=lang_id).all()
            for lang_detail in lang_details:
                db.session.delete(lang_detail)
                # print(lang_detail)
            # # Commit session.
            # db.session.commit()
            lang_title = Language.query.filter_by(id=lang_id).first()
            # # Add user to session.
            db.session.delete(lang_title)
            # Commit session.
            db.session.commit()

            return {'status': 'Deleted!'}

        except Exception as why:

            # Log the error.
            logging.error(why)

            # Return error.
            return error.INVALID_INPUT_422

class LanguageStatus(Resource):
    # @auth.login_required
    # @role_required.permission(2)
    def get(self):
        try:
            languages = Language.query.filter_by(status=1).all()
            
            # Create user schema for serializing.
            language_schema = LanguageSchema(many=True)

            # Get json data
            data = language_schema.dump(languages)
            # Return json data from db.
            return data

        except Exception as why:

            # Log the error.
            logging.error(why)

            # Return error.
            return error.INVALID_INPUT_422
    def post(self):
        try:
            # get data
            id, status = request.json.get('id'), request.json.get('status')
            print('id is')
            print(id)
        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("data wrong. " + str(why))
            # Return invalid input error.
            return error.INVALID_INPUT_422
        # check if data is existed
        data = Language.query.filter_by(id=id).first()
        if data is not None:
            # return error.ALREADY_EXIST
            data.status = status
            db.session.commit()
            return {'status': 'Updated Successfully!'}
        else:
            return error.INVALID_INPUT_422

