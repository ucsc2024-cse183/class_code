from .common import db, Field, auth
from pydal.validators import *
import datetime

db.define_table(
    "entry",
    Field("title", requires=IS_NOT_EMPTY()),
    Field("description", "text", requires=IS_NOT_EMPTY()),
    Field("post_date", "datetime", readable=False, writable=False, default=lambda:datetime.datetime.now()),
    Field("author", "reference auth_user", readable=False, writable=False, default=lambda:auth.user_id),
    Field("votes", "integer", readable=False, writable=False, default=0),
)

db.define_table(
    "comment",
    Field("entry_id", "reference entry", readable=False, writable=False),
    Field("body", requires=IS_NOT_EMPTY()),
    Field("post_date", "datetime", readable=False, writable=False, default=lambda:datetime.datetime.now()),
    Field("author", "reference auth_user", readable=False, writable=False, default=lambda:auth.user_id),
)

