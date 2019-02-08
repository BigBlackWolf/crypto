from app import views


def setup_routes(app):
    app.add_url_rule('/', view_func=views.GenerateHandler.as_view('generate'))
    app.add_url_rule('/encrypt', view_func=views.EncryptHandler.as_view('encrypt'))
    app.add_url_rule('/decrypt', view_func=views.DecryptHandler.as_view('decrypt'))
    app.add_url_rule('/signature', view_func=views.SignatureHandler.as_view('signature'))
    app.add_url_rule('/verify', view_func=views.VerifyHandler.as_view('verify'))
    app.add_url_rule('/send', view_func=views.SendHandler.as_view('send'))
    app.add_url_rule('/receive', view_func=views.ReceiveHandler.as_view('receive'))
    app.add_url_rule('/api/random', view_func=views.APIView.as_view('random'))
