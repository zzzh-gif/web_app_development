from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.parking import ParkingLot
from app.models.payment import Payment, MonthlyPass
import logging
from datetime import datetime, timezone

parking_bp = Blueprint('parking', __name__)

@parking_bp.route('/api/parking/status', methods=['GET'])
def get_parking_status():
    """取得所有停車場的最新狀態與剩餘車位數"""
    try:
        lots = ParkingLot.get_all()
        data = [{
            'id': lot.id,
            'name': lot.name,
            'total_spaces': lot.total_spaces,
            'available_spaces': lot.available_spaces,
            'latitude': lot.latitude,
            'longitude': lot.longitude,
            'rate_per_hour': lot.rate_per_hour
        } for lot in lots]
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        logging.error(f"Error in get_parking_status: {e}")
        return jsonify({"status": "error", "message": "Failed to fetch parking status"}), 500

@parking_bp.route('/parking/pay', methods=['GET', 'POST'])
def view_pay_form():
    """顯示與接收繳費表單"""
    if request.method == 'POST':
        license_plate = request.form.get('license_plate')
        if not license_plate:
            flash("請輸入有效的車牌號碼！", "danger")
            return redirect(url_for('parking.view_pay_form'))
        
        flash(f"已查詢車牌: {license_plate}，請確認繳費明細", "info")
        return redirect(url_for('parking.confirm_pay', plate=license_plate))
        
    return render_template('parking/pay.html')

@parking_bp.route('/parking/pay/confirm', methods=['GET', 'POST'])
def confirm_pay():
    """確認繳費資訊並授權付款"""
    plate = request.args.get('plate', '')
    if request.method == 'POST':
        license_plate = request.form.get('license_plate')
        if not license_plate:
            flash("車牌資料遺失，請重新操作", "danger")
            return redirect(url_for('parking.view_pay_form'))
        
        try:
            # MVP: 動態抓取第一座停車場作為 Mock 資料
            lots = ParkingLot.get_all()
            if not lots:
                flash("系統無任何停車場記錄，無法繳費。", "danger")
                return redirect(url_for('main.index'))
                
            lot = lots[0]
            payment = Payment.create(
                parking_lot_id=lot.id,
                license_plate=license_plate,
                amount=50, # Mock 金額
                payment_type='hourly',
                entry_time=datetime.now(timezone.utc).isoformat()
            )
            payment.mark_as_paid()
            flash("繳費成功！感謝您的使用。", "success")
            return redirect(url_for('main.index'))
        except Exception as e:
            logging.error(f"Payment failed: {e}")
            flash("繳費處理發生異常，請稍後再試。", "danger")
            return redirect(url_for('parking.view_pay_form'))
            
    return render_template('parking/confirm.html', plate=plate)

@parking_bp.route('/parking/monthly', methods=['GET', 'POST'])
def monthly_pass_form():
    """處理月租停車位申請"""
    lots = ParkingLot.get_all()
    if request.method == 'POST':
        license_plate = request.form.get('license_plate')
        parking_lot_id = request.form.get('parking_lot_id')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        
        if not all([license_plate, parking_lot_id, start_date, end_date]):
            flash("請填寫所有必填欄位！", "danger")
            return redirect(url_for('parking.monthly_pass_form'))
            
        try:
            MonthlyPass.create(
                user_id=1, # Mock User ID for MVP
                parking_lot_id=parking_lot_id,
                license_plate=license_plate,
                start_date=start_date,
                end_date=end_date
            )
            flash("月租申請成功！", "success")
            return redirect(url_for('main.index'))
        except Exception as e:
            logging.error(f"Monthly pass application failed: {e}")
            flash("申請發生錯誤，請通知管理員。", "danger")
            return redirect(url_for('parking.monthly_pass_form'))
            
    return render_template('parking/monthly.html', lots=lots)
