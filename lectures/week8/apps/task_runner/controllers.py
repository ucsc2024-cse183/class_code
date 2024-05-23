
from py4web import action, request, abort, redirect, URL, Field
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.form import Form

@action("index", method=["GET","POST"])
@action.uses("generic.html", auth.user)
def index():
    form = Form([Field("task_name"), Field("sleep_time", "integer")])
    if form.accepted:
        db.mytask.insert(name=form.vars["task_name"],
                         task_info={"function": "task1", "inputs": {"x": form.vars["sleep_time"]}})
        # start or record the task
        redirect(URL("task_recorded"))
    return locals()


@action("task_recorded")
@action.uses("generic.html", auth.user)
def task_recorded():
    message = "you task was recorded"
    return locals()    
