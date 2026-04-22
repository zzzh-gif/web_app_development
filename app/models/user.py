from datetime import datetime, timezone
from app.models import db
import logging

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    default_license_plate = db.Column(db.String(20), nullable=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.String(50), default=lambda: datetime.now(timezone.utc).isoformat(), nullable=False)

    @classmethod
    def create(cls, username, email, password_hash, default_license_plate=None):
        """新增一筆使用者記錄"""
        try:
            new_user = cls(
                username=username,
                email=email,
                password_hash=password_hash,
                default_license_plate=default_license_plate
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating User: {e}")
            raise

    @classmethod
    def get_by_id(cls, user_id):
        """根據 ID 取得單筆使用者記錄"""
        try:
            return cls.query.get(user_id)
        except Exception as e:
            logging.error(f"Error getting User by id: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有使用者記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            logging.error(f"Error getting all Users: {e}")
            return []

    def update(self, **kwargs):
        """更新使用者記錄"""
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating User: {e}")
            raise

    def delete(self):
        """刪除使用者記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting User: {e}")
            raise
