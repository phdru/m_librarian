from bottle import route


@route('/')
def hello():
    return "Hello World!"
