
from flask_socketio import SocketIO, emit
from flask import request
from flask_login import current_user

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    if not current_user.is_authenticated:
        return False
    emit('status', {'msg': f'{current_user.email} connected'})

@socketio.on('location_update')
def handle_location(data):
    emit('new_location', data, broadcast=True)
