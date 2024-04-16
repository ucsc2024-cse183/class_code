from py4web import action

@action("index")
@action.uses("index.html")
def index():
    return {"message": "cse183"}

@action("welcome")
def welcome(name="everybody"):
    return f"hello {name}!"

@action("error")
def error():
    1/0