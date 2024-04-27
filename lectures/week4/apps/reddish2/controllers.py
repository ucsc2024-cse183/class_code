from py4web import action, request, abort, redirect, URL
from py4web.utils.form import Form
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash

@action("index")
@action.uses("index.html", auth.user)
def index():
    return {}

@action("api/entries", method="GET")
@action.uses(db)
def _():
    rows = db(db.entry).select(orderby=~db.entry.post_date, limitby=(0,100))
    return {"entries": rows.as_list()}

@action("api/entries", method="POST")
@action.uses(db, auth.user)
def _():
    return db.entry.validate_and_insert(**request.json)

@action("api/entries/<entry_id>", method="GET")
@action.uses(db)
def _(entry_id):
    rows = db(db.entry.id==entry_id).select()
    return {"entries": rows.as_list()}

@action("api/entries/<entry_id>", method="DELETE")
@action.uses(db, auth.user)
def _():
    db(db.entry.id==entry_id).delete()
    return {}

@action("api/entries/<entry_id>", method="PUT")
@action.uses(db, auth.user)
def _(entry_id):
    return db(db.entry.id==entry_id).validate_and_update(**request.json)

@action("api/entries/<entry_id>/comments", method="GET")
@action.uses(db)
def _(entry_id):
    rows = db(db.comment.entry_id==entry_id).select(orderby=db.comment.post_date)
    return {"comments": rows.as_list()}

@action("api/entries/<entry_id>/comments", method="POST")
@action.uses(db,auth.user)
def _(entry_id):
    db.comment.entry_id.default = entry_id
    return db.comment.validate_and_insert(**request.json)



