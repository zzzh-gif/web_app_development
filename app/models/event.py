from datetime import datetime, timezone
from app.models import db
import logging

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
        """新增一筆交管與活動記錄"""
        try:
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
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating Event: {e}")
            raise

    @classmethod
    def get_by_id(cls, event_id):
        """根據 ID 取得單筆交管或活動記錄"""
        try:
            return cls.query.get(event_id)
        except Exception as e:
            logging.error(f"Error getting Event by id: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有交管或活動記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            logging.error(f"Error getting all Events: {e}")
            return []

    def update(self, **kwargs):
        """更新交管或活動記錄"""
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating Event: {e}")
            raise

    def delete(self):
        """刪除交管或活動記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting Event: {e}")
            raise
