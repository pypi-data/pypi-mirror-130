# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

import logging
from sweetrpg_model_core.model.base import EmbeddedModel


class Contribution(EmbeddedModel):
    """A model object representing contributions to an RPG volume."""

    def __init__(self, *args, **kwargs):
        """Creates a new Contribution object.

        :key str person_id: The identifier of the contributor.
        :key list roles: A list of role values indicating the contributions.
        """
        logging.debug("args: %s, kwargs: %s", args, kwargs)
        print(kwargs)  # TODO: remove

        super().__init__(*args, **kwargs)

        self.person_id = kwargs.get("person_id")
        self.roles = kwargs.get("roles")
