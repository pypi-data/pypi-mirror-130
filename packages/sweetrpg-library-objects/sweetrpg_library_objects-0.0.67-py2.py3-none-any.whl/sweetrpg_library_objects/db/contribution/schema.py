# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow import fields
from sweetrpg_library_objects.model.contribution import Contribution
from sweetrpg_model_core.schema.base import BaseEmbeddedSchema


class ContributionSchema(BaseEmbeddedSchema):
    model_class = Contribution

    person_id = fields.String(required=True)  # , load_only=True)
    roles = fields.List(fields.String(required=True))
