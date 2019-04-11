def index():
    return "Hello World!"


def register_routes(app):
    app.add_url_rule('/', methods=['get'], view_func=index)
