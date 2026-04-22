from flask import Blueprint, jsonify

transit_bp = Blueprint('transit', __name__)

@transit_bp.route('/api/transit/options', methods=['GET'])
def get_transit_options():
    """查詢遠端替代停車點與推薦的接駁轉乘資訊"""
    # MVP Mock Data
    options = [
        {
            "parking_location": "水湳經貿園區公有停車場",
            "shuttle_bus": "校園接駁車 A 線",
            "frequency_mins": 15
        },
        {
            "parking_location": "秋紅谷地下停車場",
            "shuttle_bus": "市區公車 160 路",
            "frequency_mins": 20
        }
    ]
    return jsonify({"status": "success", "options": options})
