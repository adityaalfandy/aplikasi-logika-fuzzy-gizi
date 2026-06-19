from flask import Blueprint, make_response, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.health_profile import HealthProfile
from app.models.result import Result
from app.models.progress_log import ProgressLog
from app.utils.pdf_generator import create_progress_pdf

report = Blueprint('report', __name__)

@report.route('/export/pdf')
@login_required
def export_pdf():
    # Gather data
    health_profile = HealthProfile.query.filter_by(user_id=current_user.id).first()
    latest_result = Result.query.join(HealthProfile).filter(HealthProfile.user_id == current_user.id).order_by(Result.created_at.desc()).first()
    progress_logs = ProgressLog.query.filter_by(user_id=current_user.id).order_by(ProgressLog.tanggal.asc()).all()
    
    if not health_profile:
        flash('Silakan isi profil kesehatan terlebih dahulu melalui Kalkulator.', 'error')
        return redirect(url_for('main.calculator'))
        
    try:
        pdf_bytes = create_progress_pdf(current_user, health_profile, latest_result, progress_logs)
        
        response = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=NutriWise_Report_{current_user.nama}.pdf'
        return response
    except Exception as e:
        flash(f'Gagal menggenerate PDF: {str(e)}', 'error')
        return redirect(url_for('progress.dashboard'))
