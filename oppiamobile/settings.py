
# Import settings_base.py
try:
    from oppiamobile.settings_base import *
except ImportError:
    raise ImportError("settings_base.py file could not be found.")

# Import secret_settings.py (if exists)
# > see settings_secret.py.template for reference
try:
    from oppiamobile.settings_secret import *
except ImportError:
    print("settings_secret.py file could not be found.")
