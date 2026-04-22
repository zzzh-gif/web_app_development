from datetime import datetime, timezone
from app.models import db

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.String(50), nullable=False)
    end_time = db.Column(db.String(50), nullable=False)
    affected_area = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.String(50), default=lambda: datetime.now(timezone.utc).isoformat(), nullable=False)

    @classmethod
    def create(cls, title, start_time, end_time, description=None, affected_area=None):
        new_event = cls(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            affected_area=affected_area
        )
        db.session.add(new_event)
        db.session.commit()
        return new_event

    @classmethod
    def get_by_id(cls, event_id):
        return cls.query.get(event_id)

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
