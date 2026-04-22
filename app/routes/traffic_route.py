from flask import Blueprint, jsonify, request
from app.models.event import Event
import logging

traffic_bp = Blueprint('traffic', __name__)

@traffic_bp.route('/api/route/drive', methods=['GET'])
def get_drive_route():
    """給定起訖點，回傳避走壅塞之車行路徑（回傳 JSON 供地圖繪圖）"""
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    if not origin or not destination:
        return jsonify({"status": "error", "message": "Missing origin or destination"}), 400
    
    # MVP 階段 Mock 行走點座標
    route = [
        {"lat": 24.178, "lng": 120.646, "instruction": "避開逢甲大學正門壅塞圈"},
        {"lat": 24.180, "lng": 120.648, "instruction": "轉入安全替代道路"}
    ]
    return jsonify({"status": "success", "route": route})

@traffic_bp.route('/api/events/traffic', methods=['GET'])
def get_traffic_events():
    """取得目前大型活動或校園交管（回傳 JSON 供地圖警告標定）"""
    try:
        events = Event.get_all()
        data = [{
            "id": e.id,
            "title": e.title,
            "start_time": e.start_time,
            "end_time": e.end_time,
            "affected_area": e.affected_area
        } for e in events]
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        logging.error(f"Failed to fetch traffic events: {e}")
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
