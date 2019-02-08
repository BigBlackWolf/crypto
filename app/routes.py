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
    app.add_url_rule('/api/encrypt', view_func=views.EncryptAPIView.as_view('enc'))
    app.add_url_rule('/api/decrypt', view_func=views.DecryptAPIView.as_view('dec'))
    app.add_url_rule('/api/sign', view_func=views.SignatureAPIView.as_view('sign'))
    app.add_url_rule('/api/verify', view_func=views.VerifyAPIView.as_view('ver'))
    app.add_url_rule('/api/send', view_func=views.SendAPIView.as_view('se'))
    app.add_url_rule('/api/receive', view_func=views.ReceiveAPIView.as_view('rec'))
