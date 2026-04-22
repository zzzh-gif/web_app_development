from flask import Blueprint, jsonify

transit_bp = Blueprint('transit', __name__)

@transit_bp.route('/api/transit/options', methods=['GET'])
def get_transit_options():
    """
    查詢遠端替代停車點與推薦的公車/接駁車轉乘方案。
    - HTTP 請求: GET
    - 回傳: JSON 格式轉乘建議
    """
    pass
