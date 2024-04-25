# using the browser console as your friend

```
function post(url, data) {
    var options = { method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)};
    fetch(url, options).then(r=>r.json()).then(console.log);
}          
```

# Using the DAL

Import the Database Abstraction Layer (DAL) and Field object

```
from pydal import DAL, Field
```

create a database connection (in py4web this is done for you in common.py)

```
db = DAL(uri)
db = DAL("sqlite://storage.sqlite")
db.define_table("this", Field("name"))
```

Examples of database operation:

- insert in a table        => db.{tablename}.insert(name="chair")
- update a set of records  => db(query).update(name="Chair")
- delete a set of records  => db(query).delete()
- select a set of records  => db(query).select(...)

Example of query

```
db.thing.name == "chair"
```

Examples of more complex queries

Example of Joins

Converting to list and dict



