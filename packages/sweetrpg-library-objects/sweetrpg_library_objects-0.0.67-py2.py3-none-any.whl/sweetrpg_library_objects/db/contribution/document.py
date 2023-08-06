# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from datetime import datetime
from mongoengine import EmbeddedDocument, fields
from pymongo import ASCENDING


class ContributionDocument(EmbeddedDocument):
    """A model object representing an RPG contribution."""

    meta = {
        "indexes": [
            # {"name": "contribution_name", "fields": ["name"]},
            # {"name": "person_volume_unique", "fields": ["person_id", "volume_id"], "unique": True}
        ],
        "db_alias": "default",
        # "collection": "contributions",
        "strict": False,
    }

    # basic properties
    person_id = fields.StringField(min_length=1, max_length=30, required=True)
    roles = fields.ListField(field=fields.StringField, required=True)
