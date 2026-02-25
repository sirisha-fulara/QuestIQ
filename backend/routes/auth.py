from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from extensions import db
from models.user import User

auth_bp= Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data= request.json
    username= data.get('username')
    email= data.get('email')
    password= data.get('password')
    
    if not username or not email or not password:
        return jsonify({'message':'All fields are required'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message':'User already exists'}), 409
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message':'Username already taken'}), 409

    
    hashed_password= generate_password_hash(password)
    new_user= User(
        username= username,
        email= email,
        password= hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'User registeres successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data= request.json
    email= data.get('email')
    password= data.get('password')
    
    user= User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message':'Invalid creds'})
    
    access_token= create_access_token(identity=str(user.id))
    return jsonify({
        'access_token': access_token,
        'user_id': user.id
    })