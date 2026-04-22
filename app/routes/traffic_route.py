from flask import Blueprint, jsonify, request

traffic_bp = Blueprint('traffic', __name__)

@traffic_bp.route('/api/route/drive', methods=['GET'])
def get_drive_route():
    """
    給定起訖點，回傳避開主要幹道壅塞路段之導航路徑點座標。
    - URL 參數: origin, destination
    - HTTP 請求: GET
    - 回傳: JSON 格式路由資訊
    """
    pass

@traffic_bp.route('/api/events/traffic', methods=['GET'])
def get_traffic_events():
    """
    取得目前正在進行中的大型活動、交管或封閉區域資訊。
    - HTTP 請求: GET
    - 回傳: JSON 格式事件資訊
    """
    pass
