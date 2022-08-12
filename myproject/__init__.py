import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_socketio import SocketIO


app = Flask(__name__)
# app.config['FLASK_ADMIN_SWATCH'] = 'Cyborg'


# --------------- DATABASE
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'mykeyasdfghjklsdfghnjm'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://CodeXz:hpprobook450g3*@127.0.0.1/chat_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WHOOSH_BASE'] = 'whoosh'
app.config['WHOOSH_INDEX_PATH'] = 'whoo'

# --------------- BUILD
db = SQLAlchemy(app)
Migrate(app, db)
socketio = SocketIO(app)


login = LoginManager()
login.init_app(app)
login.login_view = 'main.login'

from myproject.main.main import main
from myproject.messaging.messaging import messaging

app.register_blueprint(messaging)
app.register_blueprint(main)

# if __name__ == '__main__':
#     socketio.run(app)
