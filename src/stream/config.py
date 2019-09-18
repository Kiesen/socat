# -*- coding: utf-8 -*-
"""
Config file contains default arguments for the
implemented api endpoints.

To overwrite the config create an config_local.py file.
"""

# Twitter configuration
TWITTER = {
    "locations": "-180,-90,180,90",
    "languages": "de",
    "track": ""
}

# Try to import local settings which can be used to override any of the above
try:
    from stream.config_local import *
except ImportError:
    pass
