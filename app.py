import os
from app import create_app
from app.models import db

# 確保所有 Models 都被載入，這樣 sqlalchemy metadata 才能順序建立關聯
from app.models.user import User
from app.models.parking import ParkingLot
from app.models.payment import Payment, MonthlyPass
from app.models.event import Event

app = create_app()

if __name__ == '__main__':
    # 確保 instance 資料夾存在，用於存放 SQLite db
    instance_path = os.path.join(os.path.dirname(__file__), 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    # 初始化資料庫 (若 schema 不存在則建立資料表)
    with app.app_context():
        db.create_all()

    app.run(debug=True)
