#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

from flask import g

from api.conf.auth import auth, jwt
from api.database.database import db
from sqlalchemy.orm import relationship



class User(db.Model):

    # Generates default class name for table. For changing use
    # __tablename__ = 'users'

    # User id.
    id = db.Column(db.Integer, primary_key=True)
    # User name.
    username = db.Column(db.String(length=80))
    # User email address.
    email = db.Column(db.String(length=80))
    # User password.
    password = db.Column(db.String(length=80))
    # First name.
    first_name = db.Column(db.String(length=80))
    # Last name.
    last_name = db.Column(db.String(length=80))
    # Unless otherwise stated default role is user.
    user_role = db.Column(db.Integer)
    # User country.
    user_country = db.Column(db.Integer, db.ForeignKey('countries.id'))
    # User language.
    user_language = db.Column(db.Integer, db.ForeignKey('languages.id'))    
    # Creation time for user.
    created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    languages = relationship("Language")
    countries = relationship("Country")
    # Generates auth token.
    def generate_auth_token(self, permission_level):

        # Check if admin.
        if permission_level == 1:

            # Generate admin token with flag 1.
            token = jwt.dumps({'email': self.email, 'admin': 1})

            # Return admin flag.
            return token

            # Check if admin.
        elif permission_level == 2:

            # Generate admin token with flag 1.
            token = jwt.dumps({'email': self.email, 'admin': 2})

            # Return admin flag.
            return token

        # Return normal user flag.
        return jwt.dumps({'email': self.email, 'admin': 0})

    # Generates a new access token from refresh token.
    @staticmethod
    @auth.verify_token
    def verify_auth_token(token):

        # Create a global none user.
        g.user = None

        try:
            # Load token.
            data = jwt.loads(token)

        except:
            # If any error return false.
            return False

        # Check if email and admin permission variables are in jwt.
        if 'email' and 'admin' in data:

            # Set email from jwt.
            g.user = data['email']

            # Set admin permission from jwt.
            g.admin = data['admin']

            # Return true.
            return True

        # If does not verified, return false.
        return False

    def __repr__(self):

        # This is only for representation how you want to see user information after query.
        return "<User(id='%s', name='%s', password='%s', email='%s', created='%s')>" % (
                      self.id, self.user_country, self.user_language, self.username, self.password, self.email, self.created)


class Blacklist(db.Model):

    # Generates default class name for table. For changing use
    # __tablename__ = 'users'

    # Blacklist id.
    id = db.Column(db.Integer, primary_key=True)

    # Blacklist invalidated refresh tokens.
    refresh_token = db.Column(db.String(length=255))

    def __repr__(self):

        # This is only for representation how you want to see refresh tokens after query.
        return "<User(id='%s', refresh_token='%s', status='invalidated.')>" % (
                      self.id, self.refresh_token)

class Language(db.Model):

    __tablename__ = "languages" # table name will default to name of the model

    # Create columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # language name
    name = db.Column(db.String(length=120))
    # language foreign name
    foreign = db.Column(db.String(length=120))
    # status.
    status = db.Column(db.Boolean)
    # Creation time for languages.
    created = db.Column(db.DateTime, default=datetime.utcnow)
    # set relationship
    languages = db.relationship('LanguageDetail', backref='languages', lazy=True)
    # this is not essential, but a valuable method to overwrite as this is what we will see when we print out an instance in a REPL.
    def __repr__(self):
        return "<Language(id='%s', name='%s', foreign='%s', status='%r', created='%s')>" % (
                      self.id, self.name, self.foreign, self.status, self.created)

class Page(db.Model):

    __tablename__ = "pages" # table name will default to name of the model

    # Create columns
    id = db.Column(db.Integer, primary_key=True)
    # page name
    name = db.Column(db.String(length=120))
    # Creation time for page.
    created = db.Column(db.DateTime, default=datetime.utcnow)
    # set relationship
    pages = db.relationship('LanguageDetail', backref='pages', lazy=True)

    # this is not essential, but a valuable method to overwrite as this is what we will see when we print out an instance in a REPL.
    def __repr__(self):
        return "<Page(id='%s', name='%s', created='%s')>" % (
                      self.id, self.name, self.created)

class LanguageDetail(db.Model):

    __tablename__ = "language_details" # table name will default to name of the model

    # Create columns
    id = db.Column(db.Integer, primary_key=True)
    # page id
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
    # language id
    lang_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    # language content
    content = db.Column(db.Text)
    # language content translated
    translate = db.Column(db.Text)
    # Creation time for language details.
    created = db.Column(db.DateTime, default=datetime.utcnow)

    # this is not essential, but a valuable method to overwrite as this is what we will see when we print out an instance in a REPL.
    def __repr__(self):
        return "<LanguageDetail(id='%s', page_id='%d', lang_id='%d', content='%s', translate='%s')>" % (
                      self.id, self.page_id, self.lang_id, self.content, self.translate)

class Country(db.Model):

    __tablename__ = "countries" # table name will default to name of the model

    # Create columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # name
    name = db.Column(db.String(length=120))
    # currency
    currency = db.Column(db.String(length=50))
    # fx
    fx = db.Column(db.String(length=50))
    # land_register
    land_register = db.Column(db.Float)
    # light_of_lien
    right_of_lien = db.Column(db.Float)
    # solvency
    solvency = db.Column(db.Float)
    # abstract_lr
    abstract_lr = db.Column(db.Float)
    # valuation_fee
    valuation_fee = db.Column(db.Float)
    # solvency_rate
    solvency_rate = db.Column(db.Float)
    # reference_1
    reference_1 = db.Column(db.Float)
    # reference_2
    reference_2 = db.Column(db.Float)
    # stamp_duty
    stamp_duty = db.Column(db.Float)
    # country_costs
    country_costs = db.Column(db.Float)
    # created
    created = db.Column(db.DateTime, default=datetime.utcnow)
    # set relationship
    # countries = db.relationship('User', backref='countries', lazy=True)

    # this is not essential, but a valuable method to overwrite as this is what we will see when we print out an instance in a REPL.
    def __repr__(self):
        return "<Country(id='%s', name='%s', currency='%s', fx='%s', land_register='%f, right_of_lien='%f, solvency='%f, abstract_lr='%f, valuation_fee='%f, solvency_rate='%f, reference_1='%f, reference_2='%f, stamp_duty='%f, country_costs='%f')>" % (
                      self.id, self.name, self.currency, self.fx, self.land_register, self.right_of_lien, self.solvency, self.abstract_lr, self.valuation_fee, self.solvency_rate, self.reference_1, self.reference_2, self.stamp_duty, self.country_costs)