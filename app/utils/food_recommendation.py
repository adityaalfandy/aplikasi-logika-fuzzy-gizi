def get_food_recommendations(kalori_harian):
    # Proporsi kalori
    sarapan_cal = round(kalori_harian * 0.25)
    siang_cal = round(kalori_harian * 0.35)
    malam_cal = round(kalori_harian * 0.25)
    camilan_cal = round(kalori_harian * 0.15)
    
    # Rekomendasi sederhana (Statis untuk MVP)
    if kalori_harian < 1500:
        kategori = "Rendah Kalori (Defisit)"
        menu = {
            'sarapan': f"Oatmeal (30g) + 1 Telur Rebus + Buah Pisang (~{sarapan_cal} kkal)",
            'siang': f"Nasi Merah (100g) + Dada Ayam Panggang (100g) + Sayur Bayam (~{siang_cal} kkal)",
            'malam': f"Ikan Nila Bakar (100g) + Tumis Buncis (tanpa nasi/nasi sedikit) (~{malam_cal} kkal)",
            'camilan': f"Yogurt Plain / Buah Apel 1 buah (~{camilan_cal} kkal)"
        }
    elif 1500 <= kalori_harian <= 2200:
        kategori = "Kalori Menengah (Normal)"
        menu = {
            'sarapan': f"Roti Gandum 2 lapis + 2 Telur Orak-arik + Susu Low Fat (~{sarapan_cal} kkal)",
            'siang': f"Nasi Putih/Merah (150g) + Ayam Bakar Dada + Tumis Kangkung + Tempe (~{siang_cal} kkal)",
            'malam': f"Nasi Merah (100g) + Ikan Bakar + Salad Sayur (~{malam_cal} kkal)",
            'camilan': f"Buah Potong + Kacang Almond (15g) (~{camilan_cal} kkal)"
        }
    else:
        kategori = "Tinggi Kalori (Surplus/Aktivitas Tinggi)"
        menu = {
            'sarapan': f"Oatmeal (50g) + Susu Full Cream + 2 Telur Rebus + Selai Kacang (~{sarapan_cal} kkal)",
            'siang': f"Nasi Putih (200g) + Sapi Lada Hitam (150g) + Tahu/Tempe + Sayur (~{siang_cal} kkal)",
            'malam': f"Nasi Putih (150g) + Ayam Goreng/Bakar + Capcay Sayur (~{malam_cal} kkal)",
            'camilan': f"Smoothie Pisang + Protein Shake / Roti Lapis (~{camilan_cal} kkal)"
        }
        
        
    return {
        'kategori': kategori,
        'menu': menu,
        'calories': {
            'sarapan': sarapan_cal,
            'siang': siang_cal,
            'malam': malam_cal,
            'camilan': camilan_cal
        }
    }
