from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.form import Form

@action("index")
@action.uses("generic.html", auth, T, db)
def index():
    form = Form(db.manage)
    return locals()
