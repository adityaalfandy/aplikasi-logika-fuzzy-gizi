import os
import io
import matplotlib
matplotlib.use('Agg') # Backend for non-GUI use
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from datetime import datetime

def create_progress_pdf(user, health_profile, latest_result, progress_logs):
    # Buffer to hold PDF
    buffer = io.BytesIO()
    
    # Document settings
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenterTitle', parent=styles['Heading1'], alignment=1))
    styles.add(ParagraphStyle(name='NormalCenter', parent=styles['Normal'], alignment=1))
    
    Story = []
    
    # Header
    Story.append(Paragraph(f"<b>Laporan Progress Nutrisi NutriWise AI</b>", styles['CenterTitle']))
    Story.append(Spacer(1, 12))
    Story.append(Paragraph(f"Dihasilkan pada: {datetime.now().strftime('%d %B %Y, %H:%M')}", styles['NormalCenter']))
    Story.append(Spacer(1, 24))
    
    # Profil Pengguna
    Story.append(Paragraph("<b>Profil Pengguna</b>", styles['Heading2']))
    Story.append(Spacer(1, 6))
    
    user_info = [
        ["Nama", ":", user.nama],
        ["Email", ":", user.email],
        ["Umur", ":", f"{health_profile.umur} Tahun" if health_profile else "N/A"],
        ["Jenis Kelamin", ":", "Laki-laki" if health_profile and health_profile.jenis_kelamin == 'L' else "Perempuan"],
        ["Berat Awal", ":", f"{health_profile.berat_badan} kg" if health_profile else "N/A"],
        ["Tinggi Badan", ":", f"{health_profile.tinggi_badan} cm" if health_profile else "N/A"]
    ]
    t = Table(user_info, colWidths=[100, 20, 300])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 24))
    
    # Target Kalori AI
    if latest_result:
        Story.append(Paragraph("<b>Target Kalori AI (Fuzzy Logic)</b>", styles['Heading2']))
        Story.append(Spacer(1, 6))
        Story.append(Paragraph(f"Target Kalori Harian: <b>{latest_result.kalori_fuzzy} kkal</b>", styles['Normal']))
        Story.append(Paragraph(f"BMI Saat Ini: {latest_result.bmi} ({latest_result.status_bmi})", styles['Normal']))
        Story.append(Spacer(1, 24))
    
    # Generate Chart if logs exist
    if progress_logs:
        dates = [log.tanggal.strftime('%d/%m') for log in progress_logs]
        weights = [float(log.berat_badan) for log in progress_logs]
        cals = [log.kalori_aktual for log in progress_logs]
        targets = [log.target_kalori for log in progress_logs]
        
        plt.figure(figsize=(8, 4))
        
        # Subplot 1: Weight
        plt.subplot(1, 2, 1)
        plt.plot(dates, weights, marker='o', color='blue', linestyle='-')
        plt.title('Progress Berat Badan (kg)')
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Subplot 2: Calories
        plt.subplot(1, 2, 2)
        plt.bar(dates, cals, color='green', alpha=0.6, label='Aktual')
        plt.plot(dates, targets, color='orange', linestyle='--', marker='x', label='Target')
        plt.title('Konsumsi Kalori (kkal)')
        plt.xticks(rotation=45)
        plt.legend()
        
        plt.tight_layout()
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        plt.close()
        
        # Add Image to PDF
        Story.append(Paragraph("<b>Grafik Progress</b>", styles['Heading2']))
        Story.append(Spacer(1, 12))
        img = Image(img_buffer, width=450, height=225)
        Story.append(img)
        Story.append(Spacer(1, 24))
        
        # Log Table
        Story.append(Paragraph("<b>Riwayat Harian</b>", styles['Heading2']))
        Story.append(Spacer(1, 12))
        
        table_data = [["Tanggal", "Berat (kg)", "Kalori Aktual", "Target", "Status"]]
        for log in progress_logs:
            status = "Surplus" if log.kalori_aktual > log.target_kalori else "Defisit"
            table_data.append([
                log.tanggal.strftime('%d/%m/%Y'),
                str(log.berat_badan),
                str(log.kalori_aktual),
                str(log.target_kalori),
                status
            ])
            
        t2 = Table(table_data, colWidths=[80, 80, 80, 80, 80])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
        ]))
        Story.append(t2)
    else:
        Story.append(Paragraph("Belum ada data progress untuk ditampilkan.", styles['Normal']))
    
    doc.build(Story)
    pdf_out = buffer.getvalue()
    buffer.close()
    return pdf_out
