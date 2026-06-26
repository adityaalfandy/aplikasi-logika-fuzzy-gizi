from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.forms import CalculatorForm
from app.utils.nutrition import calculate_bmi, get_bmi_status, get_ideal_weight, calculate_bmr, calculate_tdee, calculate_macros
from app.fuzzy.engine import FuzzySugenoEngine
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == 'GET' and not request.args.get('new'):
        if 'result_data' in session:
            flash("Menampilkan hasil perhitungan terakhir Anda. Klik 'Hitung Ulang' jika ingin mengubah data.", "info")
            return redirect(url_for('main.result'))
            
    form = CalculatorForm()
    
    if request.method == 'GET':
        from flask_login import current_user
        from app.models.health_profile import HealthProfile
        if current_user.is_authenticated:
            latest_profile = HealthProfile.query.filter_by(user_id=current_user.id).order_by(HealthProfile.created_at.desc()).first()
            if latest_profile:
                form.nama.data = current_user.nama
                form.umur.data = latest_profile.umur
                form.jenis_kelamin.data = latest_profile.jenis_kelamin
                form.berat_badan.data = float(latest_profile.berat_badan)
                form.tinggi_badan.data = latest_profile.tinggi_badan
                form.aktivitas.data = latest_profile.aktivitas
                if latest_profile.alergi:
                    form.alergi.data = latest_profile.alergi.split(',')
            else:
                form.nama.data = current_user.nama
        elif 'result_data' in session:
            rd = session['result_data']
            form.nama.data = rd.get('nama')
            form.umur.data = rd.get('umur')
            form.jenis_kelamin.data = rd.get('jenis_kelamin')
            form.berat_badan.data = rd.get('berat_badan')
            form.tinggi_badan.data = rd.get('tinggi_badan')
            form.aktivitas.data = rd.get('aktivitas')
            if rd.get('alergi'):
                form.alergi.data = rd.get('alergi').split(',')

    if form.validate_on_submit():
        from flask_login import current_user
        if current_user.is_authenticated:
            nama = current_user.nama
        else:
            nama = form.nama.data
            if not nama:
                flash("Nama harus diisi.", "error")
                return render_template('calculator.html', form=form)
                
        umur = form.umur.data
        jenis_kelamin = form.jenis_kelamin.data
        berat_badan = form.berat_badan.data
        tinggi_badan = form.tinggi_badan.data
        aktivitas = form.aktivitas.data
        
        alergi_list = form.alergi.data
        alergi_str = ','.join(alergi_list) if alergi_list else None
        
        # Kalkulasi Nutrisi Dasar
        bmi = calculate_bmi(berat_badan, tinggi_badan)
        status_bmi = get_bmi_status(bmi)
        berat_ideal = get_ideal_weight(tinggi_badan, jenis_kelamin)
        bmr = calculate_bmr(berat_badan, tinggi_badan, umur, jenis_kelamin)
        kalori_tdee = calculate_tdee(bmr, aktivitas)
        
        # Fuzzy Engine
        engine = FuzzySugenoEngine()
        
        # Map aktivitas value to matching strings in fuzzy membership
        # 'sedentary', 'lightly', 'moderately', 'very', 'extra' -> we need numerical multiplier for fuzzy
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
        
        # Calculate Macros based on fuzzy calories (or TDEE if you prefer, but we'll use fuzzy)
        protein_g, lemak_g, karbo_g = calculate_macros(kalori_fuzzy)
        
        # Simpan ke Database
        from app.models.health_profile import HealthProfile
        from app.models.result import Result
        from app import db
        from flask_login import current_user
        
        profile = HealthProfile(
            user_id=current_user.id if current_user.is_authenticated else None,
            nama_guest=nama if not current_user.is_authenticated else None,
            berat_badan=berat_badan,
            tinggi_badan=tinggi_badan,
            umur=umur,
            jenis_kelamin=jenis_kelamin,
            aktivitas=aktivitas,
            alergi=alergi_str
        )
        db.session.add(profile)
        db.session.commit() # Commit untuk dapatkan profile.id
        
        result_db = Result(
            profile_id=profile.id,
            bmi=bmi,
            status_bmi=status_bmi,
            kalori_tdee=kalori_tdee,
            kalori_fuzzy=kalori_fuzzy,
            protein_g=protein_g,
            lemak_g=lemak_g,
            karbo_g=karbo_g,
            fuzzy_detail=fuzzy_result
        )
        db.session.add(result_db)
        db.session.commit()
        
        # Store result in session to pass to result page
        from app.utils.food_recommendation import get_food_recommendations
        rekomendasi = get_food_recommendations(kalori_fuzzy, alergi_list)
        
        session['result_data'] = {
            'nama': nama,
            'umur': umur,
            'jenis_kelamin': jenis_kelamin,
            'berat_badan': berat_badan,
            'tinggi_badan': tinggi_badan,
            'aktivitas': aktivitas,
            'alergi': alergi_str,
            'bmi': bmi,
            'status_bmi': status_bmi,
            'berat_ideal': berat_ideal,
            'kalori_tdee': kalori_tdee,
            'kalori_fuzzy': kalori_fuzzy,
            'protein_g': protein_g,
            'lemak_g': lemak_g,
            'karbo_g': karbo_g,
            'fuzzy_detail': fuzzy_result,
            'rekomendasi_menu': rekomendasi
        }
        
        return redirect(url_for('main.result'))
        
    return render_template('calculator.html', form=form)

@main.route('/result')
def result():
    result_data = session.get('result_data')
    if not result_data:
        flash('Silakan isi form kalkulator terlebih dahulu.', 'warning')
        return redirect(url_for('main.calculator'))
        
    # Serialize fuzzy detail for Chart.js
    fuzzy_json = json.dumps(result_data['fuzzy_detail'])
    
    return render_template('result.html', data=result_data, fuzzy_json=fuzzy_json)
