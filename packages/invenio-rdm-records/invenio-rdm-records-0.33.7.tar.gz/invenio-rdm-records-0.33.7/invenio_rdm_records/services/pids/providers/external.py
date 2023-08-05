# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""PID Base Provider."""

from flask import current_app
from flask_babelex import lazy_gettext as _

from .base import PIDProvider


class ExternalPIDProvider(PIDProvider):
    """This provider is validates PIDs to unmanaged constraints.

    It does not support any other type of operation. However, it helps
    generalize the service code by using polymorphism.
    """

    def __init__(self, name, pid_type, **kwargs):
        """Constructor."""
        super().__init__(name, pid_type=pid_type, managed=False, **kwargs)

    def validate(
        self, record, identifier=None, provider=None, client=None, **kwargs
    ):
        """Validate the attributes of the identifier.

        :returns: A tuple (success, errors). The first specifies if the
                  validation was passed successfully. The second one is an
                  array of error messages.
        """
        if client:
            current_app.logger.error(
                "Configuration error: client attribute not supported for "
                f"provider {self.name}")
            raise  # configuration error

        success, errors = super().validate(
            record, identifier, provider, **kwargs)

        if not identifier:
            errors.append(_("PID value is required for external provider."))

        return (True, []) if not errors else (False, errors)
