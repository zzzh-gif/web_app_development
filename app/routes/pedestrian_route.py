from flask import Blueprint, jsonify, request

pedestrian_bp = Blueprint('pedestrian', __name__)

@pedestrian_bp.route('/api/route/walk', methods=['GET'])
def get_walk_route():
    """
    給定起訖點，回傳結合行人專用道與周邊商店街的心安步行路徑座標。
    - URL 參數: origin, destination
    - HTTP 請求: GET
    - 回傳: JSON 格式步行路由資訊
    """
    pass
