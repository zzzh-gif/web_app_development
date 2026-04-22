from datetime import datetime, timezone
from app.models import db
import logging

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    parking_lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    license_plate = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    payment_type = db.Column(db.String(30), nullable=False)
    entry_time = db.Column(db.String(50), nullable=False)
    exit_time = db.Column(db.String(50), nullable=True)
    paid_at = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.String(50), default=lambda: datetime.now(timezone.utc).isoformat(), nullable=False)

    user = db.relationship('User', backref=db.backref('payments', lazy=True))
    parking_lot = db.relationship('ParkingLot', backref=db.backref('payments', lazy=True))

    @classmethod
    def create(cls, parking_lot_id, license_plate, amount, payment_type, entry_time, user_id=None):
        """新增一筆繳費記錄"""
        try:
            new_payment = cls(
                parking_lot_id=parking_lot_id,
                license_plate=license_plate,
                amount=amount,
                payment_type=payment_type,
                entry_time=entry_time,
                user_id=user_id
            )
            db.session.add(new_payment)
            db.session.commit()
            return new_payment
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating Payment: {e}")
            raise

    @classmethod
    def get_by_id(cls, payment_id):
        """根據 ID 取得單筆繳費記錄"""
        try:
            return cls.query.get(payment_id)
        except Exception as e:
            logging.error(f"Error getting Payment by id: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有繳費記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            logging.error(f"Error getting all Payments: {e}")
            return []

    def update(self, **kwargs):
        """更新繳費記錄"""
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating Payment: {e}")
            raise

    def delete(self):
        """刪除繳費記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting Payment: {e}")
            raise

    def mark_as_paid(self):
        """將繳費紀錄標記為已付款"""
        try:
            self.status = 'paid'
            self.paid_at = datetime.now(timezone.utc).isoformat()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error marking Payment as paid: {e}")
            raise


class MonthlyPass(db.Model):
    __tablename__ = 'monthly_passes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parking_lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    license_plate = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.String(50), nullable=False)
    end_date = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.String(50), default=lambda: datetime.now(timezone.utc).isoformat(), nullable=False)

    user = db.relationship('User', backref=db.backref('monthly_passes', lazy=True))
    parking_lot = db.relationship('ParkingLot', backref=db.backref('monthly_passes', lazy=True))

    @classmethod
    def create(cls, user_id, parking_lot_id, license_plate, start_date, end_date):
        """新增一筆月租通行證記錄"""
        try:
            new_pass = cls(
                user_id=user_id,
                parking_lot_id=parking_lot_id,
                license_plate=license_plate,
                start_date=start_date,
                end_date=end_date
            )
            db.session.add(new_pass)
            db.session.commit()
            return new_pass
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating MonthlyPass: {e}")
            raise

    @classmethod
    def get_by_id(cls, pass_id):
        """根據 ID 取得單筆月租通行證記錄"""
        try:
            return cls.query.get(pass_id)
        except Exception as e:
            logging.error(f"Error getting MonthlyPass by id: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有月租通行證記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            logging.error(f"Error getting all MonthlyPasses: {e}")
            return []

    def update(self, **kwargs):
        """更新月租通行證記錄"""
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating MonthlyPass: {e}")
            raise

    def delete(self):
        """刪除月租通行證記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting MonthlyPass: {e}")
            raise
