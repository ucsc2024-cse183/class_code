from py4web import action, request, abort, redirect, URL
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.form import Form

@action("index", method=['GET', 'POST'])
@action.uses("index.html", session, auth, db)
def index():
    user = auth.get_user()
    message = f"hello {user['first_name'] if user else 'anonymous'}"
    form = Form(db.todo)
    items = db(db.todo).select()
    return dict(message=message, form=form, items=items)
