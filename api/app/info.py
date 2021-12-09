from flask import Blueprint, jsonify
from app.auth import token_required
from app.models import Interface, Router
from utils.json import JSONEncoder
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

        loss_12 = np.array(int_1.outPkgs) - np.array(int_2.inPkgs)
        loss_21 = np.array(int_2.outPkgs) - np.array(int_1.inPkgs)

        link_info[network] = {'interface_1': int_1.to_json(), 'interface_2': int_2.to_json(), 'loss_12': loss_12.tolist(), 'loss_21': loss_21.tolist()}
    return jsonify(link_info)