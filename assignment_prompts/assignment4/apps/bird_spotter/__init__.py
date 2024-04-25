from py4web import action

@action("index")
def index():
    return "hello world"
