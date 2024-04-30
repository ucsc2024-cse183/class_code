# models.py

We define the data structures (typically db tables)

```
from py4web import Field
# https://py4web.com/_documentation/static/en/chapter-12.html#form-validation
from pydal.validators import *
from .common import db, auth

db.define_table(
    "thing",
    Field("name", requires=IS_NOT_EMPTY()),
    Field("color", requires=IS_IN_SET(["red","green","blue"])),
    Field("weight", "float", requires=IS_FLOAT_IN_RANGE(0,100)),
    auth.signature
)
```

# controllers.py

```
from py4web import action, redirect, HTTP, URL
from .common import db, auth, session
from py4web.utils.form import Form
from py4web.utils.grid import Grid

@action("index", method="GET")        # http://{domain}/{app_name}/index -> ()
@action.uses("index.html", auth.user) # you want a user
# @action.uses(auth)                  # you do not care if you have a user
def index():
    # auth
    user = auth.get_user()            # return none if no logged in user

    # permissions
    if not user or user.email != "you@example.com":
        raise HTTP(401)               # handle permissions

    # forms
    db.thing.name.writable = False
    db.thing.name.readable = False
    db.thing.name.requires = IS_NOT_EMPTY()
    form = Form(db.thing)                # create form
    form = Form(db.thing, 2)             # update form db.thing[2]
    if form.accepted:
       recirect(URL("index"))

    # grid https://github.com/jpsteil/grid_tutorial
    # grid = Grid("/", db.thing, editable=True, deletable=True)

    # database
    rows = db(db.thing).select()      # select from database
    db.thing.insert(...)              # insert in database

    # navigation
    redirect("http://google.com")     # return HTTP 301 message goto ...
    raise HTTP(404)                   # return HTTP 404

    import math
    return {"form": form, "math": math}
#   return "hello world"
#   return locals()
```

# APIs

```
@action("api/something/<i:int>", method="GET")    # http://{domain}/{app_name}/api/something -> ()
                                                 # https://bottlepy.org/docs/dev/routing.html
@action.uses(db)                      # just use db
# @action.uses(auth)                    # try id the user
# @action.uses(auth.user)               # require a user
def api_something(i):
    # auth
    user = auth.get_user()            # return none if no logged in user

    # permissions
    if not user or user.email != "you@example.com":
        raise HTTP(401)               # handle permissions

    # database
    rows = db(db.thing).select()      # select from database
    return {"things": rows}           # returns JSON
```

for i in range(10):
    print(i, math.sin(i))

# template

```
<html>
    <body>
        [[include]]
    </body>
</html>
```

```
[[extends "layout.html"]]
<table>
    [[for in range(10):]]                        
    <tr>
        <td>[[=i]]</td><td>[[=math.sin(i)]]</td>
    </tr>
    [[pass]]
</table>
```