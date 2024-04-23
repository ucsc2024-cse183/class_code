database operation:
- insert in a table        => db.{tablename}.insert(name="chair")
- update a set of records  => db(query).update(name="Chair")
- delete a set of records  => db(query).delete()
- select a set of records  => db(query).select(...)

query
db.thing.name == "chair"