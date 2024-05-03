from py4web import action, request, abort, redirect, URL
from yatl.helpers import A, BUTTON, TABLE, TR, TD
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.form import Form
from py4web.utils.grid import Grid

@action("index", method=["GET", "POST"])
@action.uses("generic.html", db)
def index():    
    mybutton = A("create a record", _role="button", _href=URL("create"))    
    table = TABLE()
    for row in db(db.person).select():
        table.append(TR(TD(row.name), TD(A("edit", _href=URL("edit", row.id)))))
    return {"mybutton":mybutton, "table": table}

@action("create", method=["GET", "POST"])
@action.uses("generic.html", db)
def create():    
    form = Form(db.person,deletable=False,show_id=False)
    if form.accepted:
        redirect(URL("index"))
    return locals()

@action("edit/<person_id:int>", method=["GET", "POST"])
@action.uses("generic.html", db)
def edit(person_id):    
    form = Form(db.person,person_id,deletable=True,show_id=False)
    if form.accepted or form.deleted:
        redirect(URL("index"))
    return locals()

@action("manage", method="GET")
@action("manage/<path:path>", method=["POST", "GET"])
@action.uses("generic.html", db)
def manage(path=None):
    grid = Grid(path, db.person.name.startswith("M"))
    return locals()

@action("player/<filename>")
@action.uses("player.html")
def player(filename):
    return {"filename": filename}
