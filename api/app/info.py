from flask import Blueprint, jsonify, request
from app.auth import token_required
from app.models import Interface, Router
import json
import numpy as np
from bson.json_util import dumps

bp = Blueprint('info', __name__, url_prefix='/info')

@bp.route('/topology', methods=['GET'])
def getTopology():
    with open('topology.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

@bp.route('/interfaces', methods=['GET'])  
def getInputPackages():
    interfaces = Interface.objects().aggregate([
        {
            '$lookup': {
                'from': 'router',
                'localField': 'router',
                'foreignField': '_id',
                'as': 'router'
            }
        },
        {
            '$group': {
                '_id': '$router',
                'interfaces': {'$push': '$$ROOT'}
            }
        }
    ])
    interfaces = dumps(interfaces)
    return jsonify(json.loads(interfaces))

@bp.route('/interfaces/<router_id>', methods=['GET'])  
def getInputPackagesByRouter(router_id):
    interfaces = Interface.objects(router=router_id)
    return jsonify(interfaces)

@bp.route('/link', methods=['GET'])
def getLonkInfo():
    with open('connections.json', 'r') as f:
        connections = json.load(f)
    link_info = {}
    for network in connections:
        connection = connections[network]
        if len(connections[network]) < 2:
            continue
        router_1 = Router.objects(hostname=connection[0]['router']).first()
        router_2 = Router.objects(hostname=connection[1]['router']).first()
        int_1 = Interface.objects(router=router_1.id, description=connection[0]['interface']).first()
        int_2 = Interface.objects(router=router_2.id, description=connection[1]['interface']).first()

        if router_1 is None or router_2 is None or int_1 is None or int_2 is None:
            return jsonify({})

        int1_in = np.array(int_1.inPkgs)
        int1_out = np.array(int_1.outPkgs)
        int2_in = np.array(int_2.inPkgs)
        int2_out = np.array(int_2.outPkgs)

        max_12 = max(len(int1_out), len(int2_in))
        max_21 = max(len(int2_out), len(int1_in))

        loss_12 = np.pad(int1_out, (max_12 - len(int1_out), 0)) - np.pad(int2_in, (max_12 - len(int2_in), 0))
        loss_21 = np.pad(int2_out, (max_21 - len(int2_out), 0)) - np.pad(int1_in, (max_21 - len(int1_in), 0))
        
        # loss_12 = np.array(int_1.outPkgs) - np.array(int_2.inPkgs)
        # loss_21 = np.array(int_2.outPkgs) - np.array(int_1.inPkgs)

        link_info[network] = {'interface_1': int_1.to_json(), 'interface_2': int_2.to_json(), 'loss_12': loss_12.tolist(), 'loss_21': loss_21.tolist()}
    return jsonify(link_info)

# @bp.route('/router', methods=['POST'])
# def addRouter():
#     router = request.json
#     setSysName(router['ip'], router['hostname'])
#     setSysDescr(router['ip'], router['description'])
#     setSysContact(router['ip'], router['contact'])
#     setSysLocation(router['ip'], router['location'])

#     Router.objects.with_id(router['id']).modify(
#         upsert=True, new=True,
#         hostname=router['hostname'],
#         description=router['description'],
#         contact=router['contact'],
#         location=router['location']
#     )
#     router.save()
#     return jsonify(router)