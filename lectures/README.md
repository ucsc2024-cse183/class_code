# Security

## Access Control

```
db.define_table("thing", Field("name"), auth.signature)

@action("edit/<thing_id:int>")
@action.uses(auth.user) # only a logged in use can access
def edit(thing_id):

    # only selected user can access this
    selected_users = ["user1", "user2"]
    user = auth.get_user()
    if user.username not in selected_users:
        raise HTTP(401)

    # you want to allow this only if the current user has created 2
    the_thing = db.thing(thing_id, created_by=auth.user_id)
    if not the_thing:
        raise HTTP(401)

    form = Form(db.thing, the_thing)
    return locals()
```


## SQL Injections

```
>>> name = "Roland Harper"
>>> db.executesql("SELECT * FROM person WHERE name='%s';" % name)
[(1, 'Roland Harper', None, None)]
>>> name = "' OR ''='"
>>> db.executesql("SELECT * FROM person WHERE name='%s';" % name)
... get everyting ...
```

Always use an API that prevents SQL injections
```
>>> name = "' OR ''='"
>>> print(db(db.person.name == name).select())
person.id,person.name,person.age,person.color

>>> db._lastsql
('SELECT "person"."id", "person"."name", "person"."age", "person"."color" FROM "person" WHERE ("person"."name" = \'\'\' OR \'\'\'\'=\'\'\');', 0.00017118453979492188)
```

