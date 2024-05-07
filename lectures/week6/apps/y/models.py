"""
This file defines the database models
"""

from .common import db, Field, auth
from pydal.validators import *

db.define_table(
    "url_map",
    Field("long_url", requires=IS_NOT_EMPTY()),
    auth.signature,
)

if db(db.url_map).count() == 0:
    db.url_map.insert(
        long_url="https://groups.google.com/g/ucsc2024-cse183/",
    )
    db.commit()