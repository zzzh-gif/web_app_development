from datetime import datetime, timezone
from app.models import db

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

    @classmethod
    def get_by_id(cls, payment_id):
        return cls.query.get(payment_id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def mark_as_paid(self):
        self.status = 'paid'
        self.paid_at = datetime.now(timezone.utc).isoformat()
        db.session.commit()


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

    @classmethod
    def get_by_id(cls, pass_id):
        return cls.query.get(pass_id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
