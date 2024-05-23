from py4web import action, request, abort, redirect, URL, Field
from pydal.validators import IS_NOT_EMPTY, IS_INT_IN_RANGE
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.form import Form

import time

@action("index", method=["GET","POST"])
@action.uses("index.html", auth, T)
def index():
    form = Form([Field("name", requires=IS_NOT_EMPTY("Doh! Write something"))])
    if form.accepted:        
        # redirect(URL("other", vars={"name": form.vars["name"]}))
        # session.name = form.vars["name"]
        auth.flash.set("hello " + form.vars["name"])
        redirect(URL("other"))
    return dict(form=form)

@action("other", method=["GET","POST"])
@action.uses("other.html", auth, T)
def other():
    # name = request.query.get("name", "unknown")
    # return dict(name=name)
    return dict()


@action("step1", method=["GET","POST"])
@action.uses("generic.html", session)
def step1():
    # collect a
    form = Form([Field("a", "integer", requires=IS_INT_IN_RANGE(0,100))])
    if form.accepted:
        session["a"] = form.vars["a"]
        redirect(URL("step2"))
    return dict(form=form)

@action("step2", method=["GET","POST"])
@action.uses("generic.html", session)
def step2():
    print(dict(session))
    if "a" not in session:
        redirect(URL("step1"))
    # collect b
    form = Form([Field("b", "integer", requires=IS_INT_IN_RANGE(0,100))])
    if form.accepted:
        session["b"] = form.vars["b"]
        redirect(URL("step3"))
    return dict(form=form)

@action("step3", method=["GET","POST"])
@action.uses("generic.html", session)
def step3():
    if "a" not in session:
        redirect(URL("step1"))
    if "b" not in session:
        redirect(URL("step2"))
    # collect c
    form = Form([Field("c", "integer", requires=IS_INT_IN_RANGE(0,100))])
    if form.accepted:
        session["c"] = form.vars["c"]
        redirect(URL("step4"))
    return dict(form=form)

@action("step4", method=["GET","POST"])
@action.uses("generic.html", session)
def step4():
    if "a" not in session or "b" not in session or "c" not in session:
        redirect(URL("step1"))
    d = session.get("a") + session.get("b") + session.get("c")
    return dict(total = d)


    