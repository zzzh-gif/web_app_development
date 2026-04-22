from flask import Blueprint, jsonify, request

pedestrian_bp = Blueprint('pedestrian', __name__)

@pedestrian_bp.route('/api/route/walk', methods=['GET'])
def get_walk_route():
    """規劃結合商店街與行人專用道的安全步行路線"""
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    if not origin or not destination:
        return jsonify({"status": "error", "message": "Missing origin or destination"}), 400

    # MVP Mock Data
    route = [
        {"lat": 24.179, "lng": 120.647, "instruction": "走進行人專用道"},
        {"lat": 24.181, "lng": 120.649, "instruction": "順路經過逢甲文華路商圈"}
    ]
    return jsonify({"status": "success", "route": route})
