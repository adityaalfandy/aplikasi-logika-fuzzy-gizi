from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.forms import ProgressForm
from app.models.progress_log import ProgressLog
from app.models.health_profile import HealthProfile
from app.models.result import Result
from app import db
import json

progress = Blueprint('progress', __name__)

@progress.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ProgressForm()
    
    from datetime import datetime, timedelta
    date_str = request.args.get('date')
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.today().date()
    except ValueError:
        selected_date = datetime.today().date()
        
    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1)
    
    is_today = selected_date == datetime.today().date()
    date_label = "TODAY" if is_today else selected_date.strftime("%d %b %Y").upper()
    
    # Get latest result target kalori as default
    latest_result = Result.query.join(HealthProfile).filter(HealthProfile.user_id == current_user.id).order_by(Result.created_at.desc()).first()
    target_kalori = latest_result.kalori_fuzzy if latest_result else 2000

    if form.validate_on_submit():
        # Fallback to old form submit logic if used (though we use log_meal now)
        log = ProgressLog(
            user_id=current_user.id,
            tanggal=form.tanggal.data,
            berat_badan=form.berat_badan.data,
            kalori_aktual=form.kalori_aktual.data,
            target_kalori=target_kalori,
            catatan=form.catatan.data
        )
        db.session.add(log)
        db.session.commit()
        flash('Progress berhasil dicatat!', 'success')
        return redirect(url_for('progress.dashboard'))

    # Fetch history for chart
    logs = ProgressLog.query.filter_by(user_id=current_user.id).order_by(ProgressLog.tanggal.asc()).all()
    
    selected_date_logs = [log for log in logs if log.tanggal == selected_date]
    
    from collections import defaultdict
    daily_logs = defaultdict(lambda: {'kalori_aktual': 0, 'target_kalori': 0})
    
    for log in logs:
        str_date = log.tanggal.strftime('%d %b')
        daily_logs[str_date]['kalori_aktual'] += log.kalori_aktual
        # Ambil target kalori dari entri log hari tersebut
        daily_logs[str_date]['target_kalori'] = log.target_kalori
        
    dates = list(daily_logs.keys())
    calories = [daily_logs[d]['kalori_aktual'] for d in dates]
    targets = [daily_logs[d]['target_kalori'] for d in dates]

    chart_data = {
        'dates': dates,
        'calories': calories,
        'targets': targets
    }
    
    # Calculate metrics
    total_days = len(dates)
    avg_daily_kcal = int(sum(calories) / total_days) if total_days > 0 else 0
    
    # For weekly, sum of last 7 unique days
    recent_dates = dates[-7:]
    total_weekly_kcal = sum([daily_logs[d]['kalori_aktual'] for d in recent_dates])
    
    # Target achieved if actual > 0 AND actual <= target OR actual is close to target (toleransi over 5%)
    target_achieved_days = sum(1 for d in dates if 0 < daily_logs[d]['kalori_aktual'] <= (daily_logs[d]['target_kalori'] * 1.10))
    
    selected_str = selected_date.strftime('%d %b')
    selected_total = daily_logs[selected_str]['kalori_aktual'] if selected_str in daily_logs else 0
    
    # Ambil target dari log hari tersebut, jika tidak ada gunakan latest_result
    if selected_str in daily_logs and daily_logs[selected_str]['target_kalori'] > 0:
        selected_target = daily_logs[selected_str]['target_kalori']
    else:
        selected_target = target_kalori

    # Hitung makro berdasarkan selected_target (40% karbo, 30% protein, 30% lemak)
    selected_karbo = round((selected_target * 0.40) / 4, 1)
    selected_protein = round((selected_target * 0.30) / 4, 1)
    selected_lemak = round((selected_target * 0.30) / 9, 1)

    # Rekomendasi Menu
    rekomendasi_menu = None
    if latest_result and hasattr(latest_result, 'rekomendasi_menu'):
        rekomendasi_menu = latest_result.rekomendasi_menu
        
    metrics = {
        'avg_daily': avg_daily_kcal,
        'total_weekly': total_weekly_kcal,
        'target_achieved': target_achieved_days,
        'total_days': total_days,
        'selected_total': selected_total,
        'selected_target': selected_target,
        'selected_karbo': selected_karbo,
        'selected_protein': selected_protein,
        'selected_lemak': selected_lemak
    }

    return render_template('progress/dashboard.html', 
                           form=form, 
                           logs=selected_date_logs[::-1], 
                           chart_data=json.dumps(chart_data),
                           latest_result=latest_result,
                           metrics=metrics,
                           rekomendasi=rekomendasi_menu,
                           selected_date=selected_date,
                           prev_date=prev_date,
                           next_date=next_date,
                           date_label=date_label)

@progress.route('/log-meal', methods=['POST'])
@login_required
def log_meal():
    meal_name = request.form.get('meal_name')
    calories = request.form.get('calories', type=int)
    date_str = request.form.get('date')

    if not meal_name or not calories:
        flash('Data meal tidak valid.', 'danger')
        return redirect(url_for('progress.dashboard'))

    from datetime import datetime
    try:
        log_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.today().date()
    except ValueError:
        log_date = datetime.today().date()

    latest_result = Result.query.join(HealthProfile).filter(HealthProfile.user_id == current_user.id).order_by(Result.created_at.desc()).first()
    
    target_kalori = latest_result.kalori_fuzzy if latest_result else 2000
    berat_badan = latest_result.profile.berat_badan if latest_result and latest_result.profile else 0
    
    log = ProgressLog(
        user_id=current_user.id,
        tanggal=log_date,
        berat_badan=berat_badan,
        kalori_aktual=calories,
        target_kalori=target_kalori,
        catatan=meal_name
    )
    db.session.add(log)
    db.session.commit()
    flash(f'{meal_name} berhasil dicatat! (+{calories} Kcal)', 'success')
    
    return redirect(url_for('progress.dashboard', date=log_date.strftime('%Y-%m-%d')))

@progress.route('/delete-log/<int:log_id>', methods=['POST'])
@login_required
def delete_log(log_id):
    log = ProgressLog.query.get_or_404(log_id)
    
    # Keamanan: Pastikan hanya pemilik log yang bisa menghapus
    if log.user_id != current_user.id:
        flash('Akses ditolak.', 'danger')
        return redirect(url_for('progress.dashboard'))
    
    date_str = log.tanggal.strftime('%Y-%m-%d')
    meal_name = log.catatan or 'Meal Log'
    
    db.session.delete(log)
    db.session.commit()
    
    flash(f'{meal_name} berhasil dihapus.', 'success')
    return redirect(url_for('progress.dashboard', date=date_str))
