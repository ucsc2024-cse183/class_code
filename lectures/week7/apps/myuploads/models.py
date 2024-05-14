"""
This file defines the database models
"""

import uuid
from .common import db, Field
from pydal.validators import *

db.define_table(
    "myupload",
    Field("name", requires=IS_NOT_EMPTY()),
    Field("description", "text"),
    Field("code", writable=False, default=lambda:str(uuid.uuid4())),
    Field("content", "upload"),
)