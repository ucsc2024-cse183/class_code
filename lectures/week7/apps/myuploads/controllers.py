from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.form import Form
from py4web.utils.grid import Grid

@action("index")
@action.uses("index.html", auth)
def index():
    return dict()

@action("manage")
@action("manage/<path:path>")
@action.uses("manage.html", auth.user)
def manage(path=None):
    grid = Grid(path, db.myupload, create=False)
    return dict(grid=grid)

@action("create", method=["GET", "POST"])
@action.uses("create.html", auth.user)
def create():
    db.myupload.content.writable = False
    form = Form(db.myupload)
    if form.accepted:
        redirect(URL("created", form.vars["id"]))
    return dict(form=form)

@action("created/<id:int>")
@action.uses("created.html", auth.user)
def created(id):
    row = db.myupload[id]
    link = None
    if row:
        link = URL("upload", row.code, scheme=True)
    return dict(row=row, link=link)

@action("upload/<code>", method=["GET", "POST"])
@action.uses("upload.html")
def upload(code):
    db.myupload.name.writable=False
    db.myupload.description.writable=False
    db.myupload.code.writable=False
    db.myupload.code.readable=False
    row = db.myupload(code=code)
    form = Form(db.myupload, row.id, show_id=False)
    if form.accepted:
        redirect(URL("uploaded"))
    return dict(form = form)

@action("uploaded")
@action.uses("uploaded.html")
def uploaded():
    return dict()
