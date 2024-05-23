
from py4web import action, request, abort, redirect, URL, Field
from yatl.helpers import A
from pydal.validators import *
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.form import Form
from py4web.utils.grid import Grid

@action("index", method=["GET","POST"])
@action.uses("generic.html", auth.user)
def index():
    form = Form([
        Field("name", rquired=IS_NOT_EMPTY()), 
        Field("x", "float", requires=IS_FLOAT_IN_RANGE(0,10))])
    if form.accepted:
        db.mytask.insert(name=form.vars["name"],
                         task="task1",
                         input={"x": form.vars["x"]},
                         created_by=auth.user_id)
        # start or record the task
        redirect(URL("task_recorded"))
    return locals()


@action("task_recorded")
@action("task_recorded/<path:path>")
@action.uses("generic.html", auth.user)
def task_recorded(path=None):
    message = "you task was recorded"
    grid = Grid(path, db.mytask.created_by==auth.user_id)
    return locals()
