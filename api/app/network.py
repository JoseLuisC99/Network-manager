from flask import Blueprint, request, jsonify
from app.auth import token_required
from app.models import Router, RouterUser

bp = Blueprint('network', __name__, url_prefix='/network')

@bp.route('/router', methods=['GET'])
@token_required
def listRouters(current_user):
    routers = Router.objects()
    return jsonify(routers)

@bp.route('/router', methods=['POST'])
@token_required
def addRouter(current_user):
    if not current_user['admin']:
        return jsonify({'status': 'error', 'info': 'Insufficient privileges'})
    
    router = Router(**request.json)
    router.save()
    return jsonify(router)

@bp.route('/router/<id>', methods=['GET'])
@token_required
def getRouter(current_user, id):
    router = Router.objects.with_id(id)
    if router is None:
        return jsonify({'status': 'error', 'info': 'Unknown router'})
    return jsonify(router)

@bp.route('/router/<id>', methods=['PUT'])
@token_required
def editRouter(current_user, id):
    if not current_user['admin']:
        return jsonify({'status': 'error', 'info': 'Insufficient privileges'})
    
    router = Router.objects.with_id(id)
    if router is None:
        return jsonify({'status': 'error', 'info': 'Unknown router'})
    
    router.update(**request.json)
    return jsonify(Router.objects.with_id(id))

@bp.route('/router/<id>', methods=['DELETE'])
@token_required
def deleteRouter(current_user, id):
    if not current_user['admin']:
        return jsonify({'status': 'error', 'info': 'Insufficient privileges'})
    
    router = Router.objects.with_id(id)
    if router is None:
        return jsonify({'status': 'error', 'info': 'Unknown router'})
    
    router.delete()
    return jsonify({'status': 'ok'})

@bp.route('/router/<id>/user', methods=['GET'])
@token_required
def listRouterUsers(current_user, id):
    if Router.objects.with_id(id) is None:
        return jsonify({'status': 'error', 'info': 'Unknown router'})
    router_users = RouterUser.objects(router=id)
    users = []
    for user in router_users:
        users.append(user.to_json())
    return jsonify(users)

@bp.route('/router/<id>/user', methods=['POST'])
@token_required
def addNewRouterUsers(current_user, id):
    if not current_user['admin']:
        return jsonify({'status': 'error', 'info': 'Insufficient privileges'})
    if Router.objects.with_id(id) is None:
        return jsonify({'status': 'error', 'info': 'Unknown router'})
    
    user = RouterUser(**request.json, router=id)
    user.save()

    return jsonify(user.to_json())

@bp.route('/router/<id_router>/user/<id_user>', methods=['GET'])
@token_required
def getRouterUser(current_user, id_router, id_user):
    user = RouterUser.objects.with_id(id_user)
    if user is None:
        return jsonify({'status': 'error', 'info': 'Unknown user'})
    return jsonify(user.to_json())

@bp.route('/router/<id_router>/user/<id_user>', methods=['PUT'])
@token_required
def editRouterUser(current_user, id_router, id_user):
    if not current_user['admin']:
        return jsonify({'status': 'error', 'info': 'Insufficient privileges'})
    user = RouterUser.objects.with_id(id_user)
    if user is None:
        return jsonify({'status': 'error', 'info': 'Unknown user'})
    
    user.update(**request.json)
    return jsonify(RouterUser.objects.with_id(id_user).to_json())

@bp.route('/router/<id_router>/user/<id_user>', methods=['DELETE'])
@token_required
def deleteRouterUser(current_user, id_router, id_user):
    if not current_user['admin']:
        return jsonify({'status': 'error', 'info': 'Insufficient privileges'})
    
    user = RouterUser.objects.with_id(id_user)
    if user is None:
        return jsonify({'status': 'error', 'info': 'Unknown user'})
    user.delete()

    return jsonify({'status': 'ok'})