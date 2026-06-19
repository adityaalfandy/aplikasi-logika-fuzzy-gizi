from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Optional

class CalculatorForm(FlaskForm):
    nama = StringField('Nama', validators=[Optional(), Length(max=100)])
    umur = IntegerField('Umur', validators=[DataRequired(), NumberRange(min=10, max=100)])
    jenis_kelamin = SelectField('Jenis Kelamin', choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], validators=[DataRequired()])
    berat_badan = FloatField('Berat Badan (kg)', validators=[DataRequired(), NumberRange(min=20, max=300)])
    tinggi_badan = IntegerField('Tinggi Badan (cm)', validators=[DataRequired(), NumberRange(min=100, max=250)])
    aktivitas = SelectField('Aktivitas Harian', choices=[
        ('sedentary', 'Sedentary (Sangat Minim Aktivitas)'),
        ('lightly', 'Lightly Active (Olahraga Ringan 1-3x/minggu)'),
        ('moderately', 'Moderately Active (Olahraga Sedang 3-5x/minggu)'),
        ('very', 'Very Active (Olahraga Intens 6-7x/minggu)'),
        ('extra', 'Extra Active (Atlet/Pekerjaan Fisik Berat)')
    ], validators=[DataRequired()])
    submit = SubmitField('Hitung Nutrisi')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=255)])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    nama = StringField('Nama Lengkap', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Length(max=255)])
    password = StringField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Daftar')

from wtforms import DateField, TextAreaField
from datetime import datetime

class ProgressForm(FlaskForm):
    tanggal = DateField('Tanggal', validators=[DataRequired()], default=datetime.today)
    berat_badan = FloatField('Berat Badan Aktual (kg)', validators=[DataRequired(), NumberRange(min=20, max=300)])
    kalori_aktual = IntegerField('Total Kalori Dikonsumsi (kkal)', validators=[DataRequired(), NumberRange(min=500, max=10000)])
    catatan = TextAreaField('Catatan / Jurnal Harian')
    submit = SubmitField('Simpan Progress')
