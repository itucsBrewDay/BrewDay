import os
from flask import Flask
from flask_login import LoginManager

from home import site
from user import *


app = Flask(__name__)

lm = LoginManager()
@lm.user_loader
def load_user(user_id):
    return UserLogin.select_user_with_id(user_id)


def create_app():
    app.config.from_object('settings')
    app.register_blueprint(site)
    lm.init_app(app)
    lm.login_view = 'site.login_page'
    return app

if __name__ == '__main__':

    app = create_app()

    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    app.run(host='0.0.0.0', port=port, debug=debug)
