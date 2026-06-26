from app import create_app, db
from app.models.food_item import FoodItem

app = create_app()

food_data = [
    # --- KARBOHIDRAT ---
    {"nama": "Nasi Putih", "kategori": "karbo", "kalori": 130, "porsi": "100g (1 centong sedang)", "tags": "vegan"},
    {"nama": "Nasi Merah", "kategori": "karbo", "kalori": 110, "porsi": "100g (1 centong sedang)", "tags": "vegan, high_fiber"},
    {"nama": "Kentang Rebus", "kategori": "karbo", "kalori": 87, "porsi": "100g (1 buah sedang)", "tags": "vegan"},
    {"nama": "Roti Gandum", "kategori": "karbo", "kalori": 150, "porsi": "2 lembar", "tags": "vegan, contains_gluten"},
    {"nama": "Oatmeal (seduh air)", "kategori": "karbo", "kalori": 150, "porsi": "40g (4 sendok makan)", "tags": "vegan, high_fiber"},
    {"nama": "Ubi Jalar Rebus", "kategori": "karbo", "kalori": 112, "porsi": "100g", "tags": "vegan"},
    {"nama": "Singkong Rebus", "kategori": "karbo", "kalori": 160, "porsi": "100g", "tags": "vegan"},
    {"nama": "Jagung Rebus", "kategori": "karbo", "kalori": 96, "porsi": "100g (1 bonggol kecil)", "tags": "vegan"},
    {"nama": "Mie Telur Rebus", "kategori": "karbo", "kalori": 140, "porsi": "100g", "tags": "contains_gluten"},
    {"nama": "Pasta Gandum Utuh (matang)", "kategori": "karbo", "kalori": 124, "porsi": "100g", "tags": "vegan, contains_gluten"},

    # --- LAUK HEWANI (PROTEIN) ---
    {"nama": "Dada Ayam Bakar", "kategori": "lauk_hewani", "kalori": 165, "porsi": "100g (1 potong sedang)", "tags": "high_protein"},
    {"nama": "Telur Rebus", "kategori": "lauk_hewani", "kalori": 78, "porsi": "1 butir (50g)", "tags": "high_protein"},
    {"nama": "Ikan Nila Bakar", "kategori": "lauk_hewani", "kalori": 128, "porsi": "100g (1 ekor sedang)", "tags": "seafood, high_protein"},
    {"nama": "Ikan Lele Goreng", "kategori": "lauk_hewani", "kalori": 200, "porsi": "1 ekor sedang", "tags": "seafood"},
    {"nama": "Daging Sapi Lada Hitam", "kategori": "lauk_hewani", "kalori": 250, "porsi": "100g", "tags": "high_protein, red_meat"},
    {"nama": "Telur Dadar", "kategori": "lauk_hewani", "kalori": 90, "porsi": "1 butir", "tags": ""},
    {"nama": "Ayam Goreng Paha", "kategori": "lauk_hewani", "kalori": 210, "porsi": "1 potong (80g)", "tags": "high_fat"},
    {"nama": "Ikan Tuna Kaleng (dalam air)", "kategori": "lauk_hewani", "kalori": 116, "porsi": "100g", "tags": "seafood, high_protein"},
    {"nama": "Udang Rebus", "kategori": "lauk_hewani", "kalori": 99, "porsi": "100g (10-12 ekor sedang)", "tags": "seafood, high_protein"},
    {"nama": "Sate Ayam (tanpa bumbu kacang)", "kategori": "lauk_hewani", "kalori": 150, "porsi": "5 tusuk", "tags": "high_protein"},
    
    # --- LAUK NABATI (PROTEIN) ---
    {"nama": "Tempe Goreng", "kategori": "lauk_nabati", "kalori": 193, "porsi": "1 potong sedang (50g)", "tags": "vegan, high_protein"},
    {"nama": "Tahu Rebus/Kukus", "kategori": "lauk_nabati", "kalori": 78, "porsi": "1 potong besar (100g)", "tags": "vegan"},
    {"nama": "Tahu Goreng", "kategori": "lauk_nabati", "kalori": 115, "porsi": "1 potong sedang (50g)", "tags": "vegan"},
    {"nama": "Tempe Bacem", "kategori": "lauk_nabati", "kalori": 150, "porsi": "1 potong sedang", "tags": "vegan"},
    {"nama": "Kacang Merah Rebus", "kategori": "lauk_nabati", "kalori": 127, "porsi": "100g", "tags": "vegan, high_fiber"},
    {"nama": "Edamame Rebus", "kategori": "lauk_nabati", "kalori": 121, "porsi": "100g", "tags": "vegan, high_protein"},
    {"nama": "Susu Kedelai (tawar)", "kategori": "lauk_nabati", "kalori": 54, "porsi": "1 gelas (200ml)", "tags": "vegan, drink"},

    # --- SAYURAN ---
    {"nama": "Tumis Kangkung", "kategori": "sayuran", "kalori": 50, "porsi": "1 mangkuk sedang (100g)", "tags": "vegan"},
    {"nama": "Sayur Bayam Bening", "kategori": "sayuran", "kalori": 35, "porsi": "1 mangkuk sedang", "tags": "vegan, high_fiber"},
    {"nama": "Brokoli Rebus", "kategori": "sayuran", "kalori": 35, "porsi": "100g", "tags": "vegan, high_fiber"},
    {"nama": "Capcay Sayur Kuah", "kategori": "sayuran", "kalori": 60, "porsi": "1 mangkuk", "tags": "vegan"},
    {"nama": "Sayur Asem", "kategori": "sayuran", "kalori": 45, "porsi": "1 mangkuk", "tags": "vegan"},
    {"nama": "Gado-gado (bumbu dipisah/sedikit)", "kategori": "sayuran", "kalori": 150, "porsi": "1 porsi kecil", "tags": "vegan, contains_peanut"},
    {"nama": "Tumis Buncis", "kategori": "sayuran", "kalori": 55, "porsi": "1 mangkuk kecil (100g)", "tags": "vegan"},
    {"nama": "Sayur Sop Bening", "kategori": "sayuran", "kalori": 40, "porsi": "1 mangkuk", "tags": "vegan"},
    {"nama": "Wortel Rebus", "kategori": "sayuran", "kalori": 41, "porsi": "100g", "tags": "vegan"},
    {"nama": "Lalapan (Timun, Kol, Kemangi)", "kategori": "sayuran", "kalori": 15, "porsi": "1 piring kecil", "tags": "vegan"},

    # --- CAMILAN & BUAH ---
    {"nama": "Pisang Ambon", "kategori": "camilan", "kalori": 89, "porsi": "1 buah sedang (100g)", "tags": "vegan, fruit"},
    {"nama": "Apel Merah", "kategori": "camilan", "kalori": 52, "porsi": "1 buah kecil", "tags": "vegan, fruit"},
    {"nama": "Yogurt Plain", "kategori": "camilan", "kalori": 59, "porsi": "1 cup (100g)", "tags": "dairy"},
    {"nama": "Kacang Almond (panggang)", "kategori": "camilan", "kalori": 164, "porsi": "1 genggam (28g)", "tags": "vegan, contains_peanut, high_fat"},
    {"nama": "Pepaya Potong", "kategori": "camilan", "kalori": 43, "porsi": "1 mangkuk kecil (100g)", "tags": "vegan, fruit"},
    {"nama": "Jeruk Manis", "kategori": "camilan", "kalori": 47, "porsi": "1 buah sedang", "tags": "vegan, fruit"},
    {"nama": "Susu Low Fat", "kategori": "camilan", "kalori": 80, "porsi": "1 gelas (200ml)", "tags": "dairy, drink"},
    {"nama": "Smoothie Pisang (tanpa gula)", "kategori": "camilan", "kalori": 120, "porsi": "1 gelas", "tags": "vegan, drink"},
    {"nama": "Biskuit Gandum", "kategori": "camilan", "kalori": 90, "porsi": "2 keping", "tags": "vegan, contains_gluten"},
    {"nama": "Protein Shake (Whey)", "kategori": "camilan", "kalori": 110, "porsi": "1 scoop (30g) dengan air", "tags": "dairy, high_protein"}
]

def seed_database():
    with app.app_context():
        print("Menghapus data FoodItem lama (jika ada)...")
        db.session.query(FoodItem).delete()
        
        print(f"Menambahkan {len(food_data)} data makanan baru...")
        for item in food_data:
            food = FoodItem(
                nama=item['nama'],
                kategori=item['kategori'],
                kalori=item['kalori'],
                porsi=item['porsi'],
                tags=item.get('tags', '')
            )
            db.session.add(food)
        
        db.session.commit()
        print("Selesai! Database makanan berhasil diisi.")

if __name__ == '__main__':
    seed_database()
