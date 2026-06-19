def calculate_bmi(berat_kg, tinggi_cm):
    tinggi_m = tinggi_cm / 100
    bmi = berat_kg / (tinggi_m ** 2)
    return round(bmi, 1)

def get_bmi_status(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi <= 24.9:
        return 'Normal'
    elif 25 <= bmi <= 29.9:
        return 'Overweight'
    else:
        return 'Obese'

def get_ideal_weight(tinggi_cm, jenis_kelamin):
    # Rumus Broca yang dimodifikasi
    if jenis_kelamin == 'L':
        return round((tinggi_cm - 100) - ((tinggi_cm - 100) * 0.1), 1)
    else:
        return round((tinggi_cm - 100) - ((tinggi_cm - 100) * 0.15), 1)

def calculate_bmr(berat_kg, tinggi_cm, umur, jenis_kelamin):
    if jenis_kelamin == 'L':
        return (10 * berat_kg) + (6.25 * tinggi_cm) - (5 * umur) + 5
    else:
        return (10 * berat_kg) + (6.25 * tinggi_cm) - (5 * umur) - 161

def calculate_tdee(bmr, aktivitas):
    faktor = {
        'sedentary': 1.2,
        'lightly': 1.375,
        'moderately': 1.55,
        'very': 1.725,
        'extra': 1.9
    }
    return round(bmr * faktor.get(aktivitas, 1.2))

def calculate_macros(kalori):
    # Asumsi: 30% Protein, 30% Lemak, 40% Karbohidrat
    # 1g Protein = 4 kcal, 1g Lemak = 9 kcal, 1g Karbo = 4 kcal
    protein_kalori = kalori * 0.30
    lemak_kalori = kalori * 0.30
    karbo_kalori = kalori * 0.40
    
    protein_g = round(protein_kalori / 4, 1)
    lemak_g = round(lemak_kalori / 9, 1)
    karbo_g = round(karbo_kalori / 4, 1)
    
    return protein_g, lemak_g, karbo_g
