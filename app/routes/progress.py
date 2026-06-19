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
    
    # Get latest result target kalori as default
    latest_result = Result.query.join(HealthProfile).filter(HealthProfile.user_id == current_user.id).order_by(Result.created_at.desc()).first()
    target_kalori = latest_result.kalori_fuzzy if latest_result else 2000

    if form.validate_on_submit():
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
    
    dates = [log.tanggal.strftime('%d %b') for log in logs]
    weights = [float(log.berat_badan) for log in logs]
    calories = [log.kalori_aktual for log in logs]
    targets = [log.target_kalori for log in logs]

    chart_data = {
        'dates': dates,
        'weights': weights,
        'calories': calories,
        'targets': targets
    }

    return render_template('progress/dashboard.html', form=form, logs=logs[::-1], chart_data=json.dumps(chart_data))
