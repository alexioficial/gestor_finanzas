from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO
from uuid import uuid4

app = Flask(__name__)

llave = uuid4().hex
app.config.from_mapping(
    SESSION_TYPE = 'filesystem',
    SESSION_PERMANENT = True,
    SECRET_KEY = llave    
)

Session(app)
socketio = SocketIO(app)

from routes.RInicio import bp as Inicio
from routes.RAuth import bp as Auth

app.register_blueprint(Inicio)
app.register_blueprint(Auth)

if __name__ == '__main__':
    socketio.run('0.0.0.0', 7100)