# -*- coding: utf-8 -*-
__version__ = '1.0.2'

default_app_config = (
    'django_changelist_inline.apps.DjangoChangelistInlineConfig'
)

from .admin import (  # noqa: F401
    ChangelistInline,
    ChangelistInlineAdmin,
    ChangelistInlineAdminMixin,
    ChangelistInlineModelAdmin,
)
