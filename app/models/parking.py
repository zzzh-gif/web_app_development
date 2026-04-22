from datetime import datetime, timezone
from app.models import db

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

    @classmethod
    def get_by_id(cls, lot_id):
        return cls.query.get(lot_id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def update(self, **kwargs):
        kwargs['updated_at'] = datetime.now(timezone.utc).isoformat()
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update_spaces(self, available_spaces):
        self.available_spaces = available_spaces
        self.updated_at = datetime.now(timezone.utc).isoformat()
        db.session.commit()
