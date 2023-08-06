# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

import logging
from sweetrpg_model_core.model.base import Model


class Volume(Model):
    """A model object representing an RPG volume (digital or print)."""

    def __init__(self, *args, **kwargs):
        """Creates a new Volume object."""
        logging.debug("args: %s, kwargs: %s", args, kwargs)

        super().__init__(*args, **kwargs)

        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.system_id = kwargs.get("system_id")
        self.slug = kwargs.get("slug")
        self.properties = kwargs.get("properties")
        self.publisher_id = kwargs.get("publisher_id")
        self.tags = kwargs.get("tags")
        # self.contributors = kwargs.get("contributors")
        self.studio_ids = kwargs.get("studio_ids")
