# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from datetime import datetime
from mongoengine import Document, fields
from sweetrpg_library_objects.db.embedded.property.document import PropertyDocument
from sweetrpg_library_objects.db.embedded.tag.document import TagDocument


class VolumeDocument(Document):
    """A mapping object to convert MongoDB data to a Volume object."""

    meta = {
        "indexes": [
            {"name": "volume_slug", "fields": ["slug"], "unique": True},
            {"name": "volume_title", "fields": ["title"]},
            {"name": "volume_system", "fields": ["system"]},
        ],
        "db_alias": "default",
        "collection": "volumes",
        "strict": False,
    }

    # basic properties
    title = fields.StringField(required=True)
    description = fields.StringField(required=True)
    slug = fields.StringField(min_length=2, max_length=50, required=True)
    system = fields.ReferenceField("SystemDocument")
    # system_id = fields.StringField(min_length=1, max_length=20, required=True)
    properties = fields.ListField(fields.EmbeddedDocumentField(PropertyDocument))
    publisher = fields.ReferenceField("PublisherDocument")
    tags = fields.ListField(fields.EmbeddedDocumentField(TagDocument))

    # audit properties
    created_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    created_by = fields.StringField(default="system", required=True)
    updated_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    updated_by = fields.StringField(default="system", required=True)
    deleted_at = fields.DateTimeField(null=True)
    deleted_by = fields.StringField(default="system", required=True)
