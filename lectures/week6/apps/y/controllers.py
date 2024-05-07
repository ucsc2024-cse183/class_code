from py4web import action, request, redirect, URL, HTTP
from .common import auth, db
from py4web.utils.form import Form
from py4web.utils.grid import Grid
from yatl.helpers import A

@action("index")
@action.uses("index.html", auth)
def index():
    return dict()

@action("main", method=["GET","POST"])
@action.uses("main.html", auth.user)
def main():
    form = Form(db.url_map)
    if form.accepted:        
        redirect(URL("short", str(form.vars["id"])))
    return locals()

@action("short/<code:int>", method=["GET","POST"])
@action.uses("short.html", auth.user)
def short(code):
    link = URL(str(code), scheme=True)    
    return locals()

@action("<code:int>")
@action.uses(db)
def _(code):
    row = db(db.url_map.id==code).select().first()
    if not row:
        raise HTTP(404)
    redirect(row.long_url)

@action("manage")
@action("manage/<path:path>")
@action.uses("manage.html", auth.user)
def manage(path=None):
    user = auth.get_user()
    db.url_map.id.label = "Short URL"
    db.url_map.id.represent = lambda value: A(URL(str(value), scheme=True), _href=URL(str(value), scheme=True))
    db.url_map.long_url.represent = lambda value: A(value, _href=value)
    db.url_map.created_on.readable = False
    db.url_map.created_by.readable = False
    db.url_map.modified_on.readable = False
    db.url_map.modified_by.readable = False
    grid = Grid(path, db.url_map.created_by==auth.user_id, show_id=True, rows_per_page=5, details=False, editable=False, create=False)
    return locals()