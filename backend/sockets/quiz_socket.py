from flask_socketio import join_room, emit
from extensions import socketio

quiz_rooms= {}  #roomcode-state

@socketio.on('create_room')
def create_room(data):
    room_code= data['room_code']
    quiz_rooms[room_code]= {
        'participants':{},
        'current_question': 0
    }
    
    join_room(room_code)
    emit('room_created', {
        'room_code': room_code
    })

@socketio.on('join_room')
def join_quiz_room(data):
    room_code= data['room_code']
    username= data['username']
    
    if room_code not in quiz_rooms:
        emit('error', {'message': 'Room not found'})
        return
    
    quiz_rooms[room_code]['participants'][username]= 0
    join_room(room_code)
    emit('user_joined',{
        'username': username
    }, room= room_code)
    
@socketio.on('submit_answer')
def submit_answer(data):
    room_code= data['room_code']
    username= data['username']
    is_correct= data['is_correct']
    
    if is_correct:
        quiz_rooms[room_code]['participants'][username] +=1
        
    emit('score_updates', {
        'scores': quiz_rooms[room_code]['participants']
    }, room= room_code)