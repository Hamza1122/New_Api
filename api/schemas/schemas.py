#!/usr/bin/python
# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class BaseUserSchema(Schema):

    """
        Base user schema returns all fields but this was not used in user handlers.
    """

    # Schema parameters.

    id = fields.Int(dump_only=True)
    user_country = fields.Int()
    user_language = fields.Int()
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
    created = fields.Str()
    user_role = fields.Str()


class UserSchema(Schema):
    """
        User schema returns only username, email and creation time. This was used in user handlers.
    """

    # Schema parameters.
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    user_role = fields.Int()
    user_country = fields.Int()
    user_language = fields.Int()
    language = fields.Str()
    country = fields.Str()    
class LanguageSchema(Schema):
    """
        Language schema
    """

    # Schema parameters.
    id = fields.Int(dump_only=True)
    name = fields.Str()
    foreign = fields.Str()
    status = fields.Boolean()

class LanguageDetailSchema(Schema):
    """
        Language schema
    """

    # Schema parameters.
    id = fields.Int(dump_only=True)
    language_id = fields.Int()
    page_id = fields.Int()
    content = fields.Str()
    translate = fields.Str()

class CountrySchema(Schema):
    """
        Country schema
    """

    # Schema parameters.
    id = fields.Int(dump_only=True)
    name = fields.Str()
    currency = fields.Str()
    fx = fields.Str()
    land_register = fields.Float()
    right_of_lien = fields.Float()
    solvency = fields.Float()
    abstract_lr = fields.Float()
    valuation_fee = fields.Float()
    solvency_rate = fields.Float()
    reference_1 = fields.Float()
    reference_2 = fields.Float()
    stamp_duty = fields.Float()
    country_costs = fields.Float()
    
    
