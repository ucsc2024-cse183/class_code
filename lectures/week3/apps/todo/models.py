"""
This file defines the database models
"""

from .common import db, Field
from pydal.validators import *

db.define_table("todo", Field("description", requires=IS_NOT_EMPTY()))