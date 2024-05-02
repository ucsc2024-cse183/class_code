"""
This file defines the database models
"""

from py4web import URL
from .common import db, Field
from pydal.validators import *

db.define_table(
    "person",
    Field("name", requires=IS_NOT_EMPTY()),
    Field("address", requires=IS_NOT_EMPTY()),
    Field("age", "integer"),
    Field("image", "upload", download_url = lambda filename: URL('download/%s' % filename)),
)

