from py4web import action, request, abort, redirect, URL
from py4web.utils.form import Form
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash

@action("index") # http://.../reddish/index -> index() -> {..} -> filter(index.html) -> HTML output
@action.uses("index.html", db, auth)
def index():
    entries = db(db.entry).select(orderby=~db.entry.post_date, limitby=(0,100))
    return locals()

@action("post", method=["GET","POST"]) # http://.../reddish/post -> post()
@action.uses("generic.html", db, auth.user)
def post():
    form = Form(db.entry)
    if form.accepted:
        redirect(URL("index"))
    return locals()

@action("entry/<entry_id:int>", method=["GET","POST"]) # http://.../reddish/entry/{id} -> entry()
@action.uses("entry.html", db, auth)
def entry(entry_id):
    entry = db.entry(id=entry_id)
    db.comment.entry_id.default = entry_id
    form = Form(db.comment)
    comments = db(db.comment.entry_id==entry_id).select()
    return locals()

@action("vote/<entry_id:int>", method="POST") # http://.../reddish/vote/{id} -> entry()
@action.uses(db, auth)
def vote(entry_id):
    entry = db.entry(id=entry_id)
    votes = entry.votes+1
    entry.update_record(votes=votes)    
    return {"votes": votes}

