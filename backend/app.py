from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import jwt, db, socketio
from flask_socketio import SocketIO
import os

from models import User, Quiz, Question, Option, Attempt
from routes.auth import auth_bp
from routes.quiz import quiz_bp
from sockets.quiz_socket import *

port = int(os.environ.get("PORT", 5000))

socketio= SocketIO(cors_allowed_origins="*",
                   async_mode="threading")

def create_app():
    app= Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(quiz_bp)
    
    @app.route('/')
    def home():
        return {'message': "flask backend running"}
    return app

app= create_app()
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=port)