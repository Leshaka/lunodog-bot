from . import utils
from .config import cfg
from .console import Console, Log
from .database import Database as Db
from . import cfg_factory
from .client import dc

"""
This package provides core functionality of the bot:
    - bot configuration access: cfg
    - console interface: Console
    - logging: Log
    - database access: Db
    - database tables versioning and migrations
    - user configs system: cfg_factory
    - discord client access: dc
    - event system: dc.event
"""