from app import db
from datetime import datetime

class FoodItem(db.Model):
    __tablename__ = 'food_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(255), nullable=False)
    kategori = db.Column(db.String(50), nullable=False) # 'karbo', 'lauk_hewani', 'lauk_nabati', 'sayuran', 'camilan'
    kalori = db.Column(db.Integer, nullable=False)
    porsi = db.Column(db.String(100), nullable=False) # e.g., '100g', '1 mangkuk', '1 potong'
    tags = db.Column(db.String(255), nullable=True) # e.g., 'seafood, contains_peanut'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<FoodItem {self.nama} ({self.kalori} kkal)>"
