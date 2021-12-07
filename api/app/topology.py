from flask import Blueprint, request, jsonify
from app.auth import token_required
from app.models import Router, RouterUser
from scripts.router import *
from scripts.protocols import *
from scripts.users import *
from scripts.cdp import *

bp = Blueprint('topology', __name__, url_prefix='/topology')

@bp.route('/', methods=['GET'])
@token_required
def getTopology(current_user):
    main_router = Router('R1', '192.168.1.1')
    topology = get_topology(main_router)
    return jsonify({'topology': topology})