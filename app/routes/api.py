from flask import Blueprint, request, jsonify
from app.utils.nutrition import calculate_bmi, get_bmi_status, get_ideal_weight, calculate_bmr, calculate_tdee, calculate_macros
from app.fuzzy.engine import FuzzySugenoEngine

api = Blueprint('api', __name__)

@api.route('/calculate', methods=['POST'])
def calculate_api():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
        
    required_fields = ['umur', 'jenis_kelamin', 'berat_badan', 'tinggi_badan', 'aktivitas']
    if not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {", ".join(required_fields)}'}), 400
        
    umur = int(data['umur'])
    jenis_kelamin = data['jenis_kelamin']
    berat_badan = float(data['berat_badan'])
    tinggi_badan = int(data['tinggi_badan'])
    aktivitas = data['aktivitas']
    
    # Kalkulasi Nutrisi Dasar
    bmi = calculate_bmi(berat_badan, tinggi_badan)
    status_bmi = get_bmi_status(bmi)
    berat_ideal = get_ideal_weight(tinggi_badan, jenis_kelamin)
    bmr = calculate_bmr(berat_badan, tinggi_badan, umur, jenis_kelamin)
    kalori_tdee = calculate_tdee(bmr, aktivitas)
    
    # Fuzzy Engine
    engine = FuzzySugenoEngine()
    faktor_aktivitas = {
        'sedentary': 1.2,
        'lightly': 1.375,
        'moderately': 1.55,
        'very': 1.725,
        'extra': 1.9
    }
    aktivitas_val = faktor_aktivitas.get(aktivitas, 1.2)
    
    fuzzy_result = engine.calculate(bmi_val=bmi, aktivitas_val=aktivitas_val, umur_val=umur)
    kalori_fuzzy = fuzzy_result['kalori_fuzzy']
    
    protein_g, lemak_g, karbo_g = calculate_macros(kalori_fuzzy)
    
    return jsonify({
        'bmi': bmi,
        'status_bmi': status_bmi,
        'berat_ideal': berat_ideal,
        'kalori_tdee': kalori_tdee,
        'kalori_fuzzy': kalori_fuzzy,
        'makronutrien': {
            'protein_g': protein_g,
            'lemak_g': lemak_g,
            'karbo_g': karbo_g
        },
        'fuzzy_detail': fuzzy_result
    }), 200

from app.models.user import User
from app.models.result import Result
from app.models.progress_log import ProgressLog
from app import db
from sqlalchemy import func

@api.route('/dashboard/stats', methods=['GET'])
def dashboard_stats():
    # Mengambil statistik agregat
    total_users = User.query.count()
    total_calculations = Result.query.count()
    total_logs = ProgressLog.query.count()
    
    # Distribusi Status BMI
    bmi_distribution = db.session.query(
        Result.status_bmi, func.count(Result.id)
    ).group_by(Result.status_bmi).all()
    
    bmi_stats = {status: count for status, count in bmi_distribution}
    
    return jsonify({
        'total_users': total_users,
        'total_calculations': total_calculations,
        'total_progress_logs': total_logs,
        'bmi_distribution': bmi_stats
    }), 200
