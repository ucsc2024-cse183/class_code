from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash


@action("index")
@action.uses("index.html", auth, T)
def index():
    user = auth.get_user()
    message = T("Hello {first_name}").format(**user) if user else T("Hello")
    return dict(message=message)

@action("api/birds", method=["GET", "POST"])
@action.uses(db)
def api_birds():
    db.bird.insert(name="penguin")
    db.bird.insert(name="dove")
    return "got it"