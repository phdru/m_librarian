from bottle import route, cheetah_view


@route('/')
@cheetah_view('index.tmpl')
def index():
    return {}
