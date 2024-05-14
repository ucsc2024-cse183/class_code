from py4web import action, request, abort, redirect, URL
from py4web.core import Fixture
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash

@action("index")
@action.uses("index.html", auth.user)
def index():
    user = auth.get_user()
    session["x"] = 12
    return dict(message=f'hello {user["first_name"]}')

@action("say_hi")
@action.uses(session, db)
def say_hi():
    if "user" in session:
        user_id = session["user"]["id"]
        user = db(db.auth_user.id==user_id).select().first()
    return {"session": dict(session), "message": f"hi {user.first_name}"}

@action("say_hi2")
@action.uses(session) # same as @action.uses(auth.user)
def say_hi():
    if ("user" not in session or
        "id" not in session["user"] or
        db(db.auth_user.id==session["user"]["id"]).count() == 0):
        redirect("auth/login")
    return {"session": dict(session)}


