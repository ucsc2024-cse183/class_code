from py4web import action, DAL, Field

db = DAL("sqlite://storage", folder="/tmp/")

db.define_table("dog", Field("name"))

@action("index")
@action.uses(db)
def index():
    id = db.dog.insert(name="snoopy")
    return f"Hello Dog #{id}"