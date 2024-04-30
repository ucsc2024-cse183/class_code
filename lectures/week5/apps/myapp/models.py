"""
This file defines the database models
"""

from .common import db, Field
from pydal.validators import *

db.define_table(
    "person",
    Field("name", requires=IS_NOT_EMPTY()),
    Field("address", requires=IS_NOT_EMPTY()),
)

