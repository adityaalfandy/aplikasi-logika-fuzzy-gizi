from app import db
from datetime import datetime

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('health_profiles.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    bmi = db.Column(db.Numeric(4, 1), nullable=False)
    status_bmi = db.Column(db.String(20), nullable=False)
    kalori_tdee = db.Column(db.SmallInteger, nullable=False)
    kalori_fuzzy = db.Column(db.SmallInteger, nullable=False)
    protein_g = db.Column(db.Numeric(5, 1))
    lemak_g = db.Column(db.Numeric(5, 1))
    karbo_g = db.Column(db.Numeric(5, 1))
    fuzzy_detail = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
