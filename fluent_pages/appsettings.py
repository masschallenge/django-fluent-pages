"""
Overview of all settings which can be customized.
"""
import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

FLUENT_PAGES_BASE_TEMPLATE = getattr(settings, "FLUENT_PAGES_BASE_TEMPLATE", 'fluent_pages/base.html')
FLUENT_PAGES_TEMPLATE_DIR = getattr(settings, 'FLUENT_PAGES_TEMPLATE_DIR', settings.TEMPLATE_DIRS[0] if settings.TEMPLATE_DIRS else None)
FLUENT_PAGES_RELATIVE_TEMPLATE_DIR = getattr(settings, 'FLUENT_PAGES_RELATIVE_TEMPLATE_DIR', True)
AUTHZ_BACKEND_NAME = getattr(settings, 'FLUENT_PAGE_AUTHZ_BACKEND', 'fluent_pages.authz_backend.SimpleBackend')

if not FLUENT_PAGES_TEMPLATE_DIR:
    raise ImproperlyConfigured("The setting 'FLUENT_PAGES_TEMPLATE_DIR' or 'TEMPLATE_DIRS[0]' need to be defined!")
else:
    # Clean settings
    FLUENT_PAGES_TEMPLATE_DIR = FLUENT_PAGES_TEMPLATE_DIR.rstrip('/') + '/'

    # Test whether the template dir for page templates exists.
    settingName = 'TEMPLATE_DIRS[0]' if not hasattr(settings, 'FLUENT_PAGES_TEMPLATE_DIR') else 'FLUENT_PAGES_TEMPLATE_DIR'
    if not os.path.isabs(FLUENT_PAGES_TEMPLATE_DIR):
        raise ImproperlyConfigured("The setting '{0}' needs to be an absolute path!".format(settingName))
    if not os.path.exists(FLUENT_PAGES_TEMPLATE_DIR):
        raise ImproperlyConfigured("The path '{0}' in the setting '{1}' does not exist!".format(FLUENT_PAGES_TEMPLATE_DIR, settingName))


def get_page_authz_backend():
    backend_name = AUTHZ_BACKEND_NAME
    try:
        mod, attr = backend_name.rsplit('.', 1)
    except ValueError:
        msg = "Unable to import page authz backend '%s'. "
        msg += "Is it a proper dotted name?"
        raise ImproperlyConfigured(msg % backend_name)

    try:
        module = import_module(mod)
    except ImportError, e:
        msg = 'Error importing CMS authz plugin %s: "%s"'
        raise ImproperlyConfigured(msg % (backend_name, e))
    except ValueError, e:
        msg = 'Error importing CMS authz plugin. Is DEFAULT_AUTHZ_BACKEND a '
        msg += 'correct dotted pathname?'
        raise ImproperlyConfigured(msg)

    try:
        cls = getattr(module, attr)
    except AttributeError:
        msg = 'Module "%s" does not define a "%s" CMS authz backend'
        raise ImproperlyConfigured(msg % (mod, attr))

    return cls()


AUTHZ_BACKEND = get_page_authz_backend()
