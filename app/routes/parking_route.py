from flask import Blueprint, render_template, request, redirect, url_for, jsonify

parking_bp = Blueprint('parking', __name__)

@parking_bp.route('/api/parking/status', methods=['GET'])
def get_parking_status():
    """
    取得所有停車場的最新狀態與剩餘車位數。
    - HTTP 請求: GET
    - 回傳: JSON 陣列
    """
    pass

@parking_bp.route('/parking/pay', methods=['GET', 'POST'])
def view_pay_form():
    """
    顯示與接收繳費表單（輸入車牌）。
    - HTTP 請求: GET 顯示; POST 處理
    - 回傳: 渲染 parking/pay.html / 重導向至 confirm_pay
    """
    pass

@parking_bp.route('/parking/pay/confirm', methods=['GET', 'POST'])
def confirm_pay():
    """
    顯示繳費明細供確認，並提供最終授權付款機制。
    - HTTP 請求: GET 顯示; POST 處理付款
    - 回傳: 渲染 parking/confirm.html / 重導向至首頁並提示成功
    """
    pass

@parking_bp.route('/parking/monthly', methods=['GET', 'POST'])
def monthly_pass_form():
    """
    顯示與接收月租停車場的申請表單。
    - HTTP 請求: GET 顯示; POST 寫入月租申請
    - 回傳: 渲染 parking/monthly.html / 完成申請重導向
    """
    pass
