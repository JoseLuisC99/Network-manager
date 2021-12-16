from flask import Blueprint, request, jsonify
from app.auth import token_required
from app.models import Router, RouterUser
from scripts.protocols import set_rip, set_ospf, set_eigrp
from scripts.users import delete_router_user, init_ssh, create_router_user, delete_router_user
from scripts.snmp import setSysName, setSysContact, setSysLocation

bp = Blueprint('network', __name__, url_prefix='/network')

@bp.route('/configure', methods=['POST'])
@token_required
def configureNetwork(current_user):
    if not current_user['admin']:
        return jsonify({'status': 'error', 'info': 'Insufficient privileges'})
    
    routers = Router.sort_by_ip(Router.objects(), reverse=True)
    errs = 0
    print(f'Method: {request.json["method"]}')
    for router in routers:
        print(router.ip)
        if request.json['method'] == 'rip':
            resp = set_rip(router.ip)
        elif request.json['method'] == 'ospf':
            resp = set_ospf(router.ip)
        elif request.json['method'] == 'eigrp':
            resp = set_eigrp(router.ip)
        if resp['status'] == 'error':
            errs += 1
    if errs > 0:
        return jsonify({'status': 'error', 'info': f'Error rate {errs}/{len(routers)}'})
    return jsonify({'status': 'ok'})

@bp.route('/configure/users', methods=['POST'])
@token_required
def addGlobalUser(current_user):
    if not current_user['admin']:
        return jsonify({'status': 'error', 'info': 'Insufficient privileges'})
    
    routers = Router.objects()
    errors = 0
    for router in routers:
        resp = init_ssh(router.hostname, router.ip)
        if resp['status'] == 'error':
            return resp
        resp = create_router_user(router.ip, {
            'username': request.json['username'],
            'privilege': int(request.json['privilege']),
            'password': request.json['password']
        })
        if resp['status'] == 'ok':
            router_info = {
                'username': request.json['username'],
                'privilege': int(request.json['privilege']),
                'password': request.json['password'],
                'router': router.id
            }
            user = RouterUser(**router_info)
            user.save()
        elif resp['status'] == 'error':
            errors += 1
    if errors > 0:
        return jsonify({'status': 'error', 'info': f'Errors {errors}/{len(routers)}'})
    else:
        return jsonify({'status': 'ok'})

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
    router_info = request.json
    if not current_user['admin']:
        return jsonify({'status': 'error', 'info': 'Insufficient privileges'})
    router = Router.objects.with_id(id)
    if router is None:
        return jsonify({'status': 'error', 'info': 'Unknown router'})
    
    print(router_info)
    setSysName(router.ip, router_info['hostname'])
    setSysContact(router.ip, router_info['contact'])
    setSysLocation(router.ip, router_info['location'])
    # setSysDescr(router.ip, router_info['description'])

    router.update(**router_info)
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
    router = Router.objects.with_id(id)
    if router is None:
        return jsonify({'status': 'error', 'info': 'Unknown router'})
    
    resp = init_ssh(router.hostname, router.ip)
    if resp['status'] == 'error':
            return resp
    resp = create_router_user(router.ip, {
        'username': request.json['username'],
        'privilege': int(request.json['privilege']),
        'password': request.json['password']
    })
    if resp['status'] == 'ok':
        user = RouterUser(**request.json, router=id)
        user.save()
        return jsonify(user.to_json())
    else:
        return jsonify(resp)

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
    delete_router_user(user.router.ip, {
        'username': user.username,
        'privilege': user.privilege,
        'password': user.password
    })
    
    username = request.json['username']
    privilege = int(request.json['privilege'])
    password = request.json['password']
    resp = create_router_user(user.router.ip, {
        'username': username,
        'privilege': privilege,
        'password': password
    })
    if resp['status'] == 'ok':
        user.update({
            'username': username,
            'privilege': privilege,
            'password': password
        })
        return jsonify(RouterUser.objects.with_id(id_user).to_json())
    else:
        return jsonify(resp)

@bp.route('/router/<id_router>/user/<id_user>', methods=['DELETE'])
@token_required
def deleteRouterUser(current_user, id_router, id_user):
    if not current_user['admin']:
        return jsonify({'status': 'error', 'info': 'Insufficient privileges'})
    
    user = RouterUser.objects.with_id(id_user)
    if user is None:
        return jsonify({'status': 'error', 'info': 'Unknown user'})
    
    result = delete_router_user(user.router.ip, {
        'username': user.username,
        'privilege': user.privilege,
        'password': user.password
    })
    if result['status'] == 'ok':
        user.delete()
    return jsonify(result)