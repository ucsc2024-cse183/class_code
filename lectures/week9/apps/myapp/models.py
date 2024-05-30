"""
This file defines the database models
"""

from .common import db, Field
from pydal.validators import *
from py4web.utils.populate import populate

query = db.auth_user

db.define_table(
    "manage",
    Field("managed", db.auth_user, requires=IS_IN_DB(db(query), "auth_user", lambda r: f"{r.first_name} {r.last_name}")))

if db(db.auth_user).count() == 0:
    populate(db.auth_user, 100)
