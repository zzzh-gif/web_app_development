from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    渲染首頁與主要地圖介面。
    - HTTP 請求: GET
    - 渲染模板: index.html
    """
    pass
