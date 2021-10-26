import functools

from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
from app.models import User

def token_required(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'payload' in request.headers:
            token = request.headers['payload']
        if not token:
            return jsonify({'status': 'error', 'info': 'Missing token'})
        
        try:
            data = jwt.decode(token, current_app.config['JWT_KEY'], algorithms=['HS256'])
            current_user = User.objects.with_id(data['id']).to_json()
        except:
            return jsonify({'status': 'error', 'info': 'Invalid token'})
        return f(current_user, *args, **kwargs)
    return decorator
                

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    if 'username' not in request.form or 'password' not in request.form:
        return jsonify({'status': 'error', 'info': 'Invalid register info'})
    username = request.form['username']
    password = request.form['password']
    err = None

    if not username:
        err = 'Username is required'
    elif not password:
        err = 'Password is required'
    elif len(User.objects(username=username)) != 0:
        err = f'User {username} is already registered'
    
    if err is None:
        user = User(username=username, password=generate_password_hash(password))
        user.save()
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'error', 'info': err})

@bp.route('/login', methods=['POST'])
def login():
    if 'username' not in request.form or 'password' not in request.form:
        return jsonify({'status': 'error', 'info': 'Invalid login info'})
    
    username = request.form['username']
    password = request.form['password']
    
    try:
        user = User.objects.get(username=username)
    except:
        return jsonify({'status': 'error', 'info': 'Invalid username'})
    
    if check_password_hash(user.password, password):
        token = jwt.encode({'id': str(user.id), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config['JWT_KEY'], algorithm='HS256')
        return jsonify({'token': token.decode('utf8')})
    
    return jsonify({'status': 'error', 'info': 'Invalid password'})

@bp.route('/modify', methods=['PUT'])
@token_required
def modifyUser(current_user):
    user = User.objects.with_id(current_user['id'])

    user.update(**request.form)
    return jsonify({'status': 'ok'})

@bp.route('/delete', methods=['DELETE'])
@token_required
def deleteUser(current_user):
    user = User.objects.with_id(current_user['id'])
    user.delete()
    return jsonify({'status': 'ok'})
