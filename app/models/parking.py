from datetime import datetime, timezone
from app.models import db
import logging

class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    total_spaces = db.Column(db.Integer, nullable=False)
    available_spaces = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    rate_per_hour = db.Column(db.Integer, nullable=False)
    contact_info = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.String(50), default=lambda: datetime.now(timezone.utc).isoformat(), nullable=False)

    @classmethod
    def create(cls, name, total_spaces, latitude, longitude, rate_per_hour, contact_info=None):
        """新增一筆停車場記錄"""
        try:
            new_lot = cls(
                name=name,
                total_spaces=total_spaces,
                available_spaces=total_spaces, # 預設全空
                latitude=latitude,
                longitude=longitude,
                rate_per_hour=rate_per_hour,
                contact_info=contact_info
            )
            db.session.add(new_lot)
            db.session.commit()
            return new_lot
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating ParkingLot: {e}")
            raise

    @classmethod
    def get_by_id(cls, lot_id):
        """根據 ID 取得單筆停車場記錄"""
        try:
            return cls.query.get(lot_id)
        except Exception as e:
            logging.error(f"Error getting ParkingLot by id: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有停車場記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            logging.error(f"Error getting all ParkingLots: {e}")
            return []

    def update(self, **kwargs):
        """更新停車場記錄"""
        try:
            kwargs['updated_at'] = datetime.now(timezone.utc).isoformat()
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating ParkingLot: {e}")
            raise

    def delete(self):
        """刪除停車場記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting ParkingLot: {e}")
            raise

    def update_spaces(self, available_spaces):
        """更新剩餘車位數"""
        try:
            self.available_spaces = available_spaces
            self.updated_at = datetime.now(timezone.utc).isoformat()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating generic spaces for ParkingLot: {e}")
            raise
