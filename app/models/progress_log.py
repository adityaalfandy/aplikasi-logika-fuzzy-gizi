from app import db
from datetime import datetime

class ProgressLog(db.Model):
    __tablename__ = 'progress_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    berat_badan = db.Column(db.Numeric(5, 2))
    kalori_aktual = db.Column(db.SmallInteger)
    target_kalori = db.Column(db.SmallInteger)
    catatan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
