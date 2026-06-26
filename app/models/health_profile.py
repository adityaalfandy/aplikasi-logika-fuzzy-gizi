from app import db
from datetime import datetime

class HealthProfile(db.Model):
    __tablename__ = 'health_profiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    nama_guest = db.Column(db.String(100), nullable=True)
    berat_badan = db.Column(db.Numeric(5, 2), nullable=False)
    tinggi_badan = db.Column(db.SmallInteger, nullable=False)
    umur = db.Column(db.SmallInteger, nullable=False)
    jenis_kelamin = db.Column(db.Enum('L', 'P'), nullable=False)
    aktivitas = db.Column(db.Enum('sedentary', 'lightly', 'moderately', 'very', 'extra'), nullable=False)
    alergi = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    result = db.relationship('Result', backref='profile', uselist=False)
