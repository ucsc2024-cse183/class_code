from py4web import action, request, abort, redirect, URL
from py4web.utils.form import Form
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash

@action("index")
@action.uses("index.html", db, auth)
def index():
    data = db(db.entry).select()
    return locals()

@action("post", method=["GET","POST"])
@action.uses("generic.html", db, auth.user)
def post():
    form = Form(db.entry)
    if form.accepted:
        redirect(URL("index"))
    return locals()

@action("entry", method=["GET","POST"])
@action.uses("entry.html", db, auth)
def entry():
    form = Form(db.comment)
    comments = db(db.comment).select()
    return locals()
