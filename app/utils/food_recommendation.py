import random
from app.models.food_item import FoodItem
from sqlalchemy import not_, or_

def get_random_food(kategori_list, alergi_list=None):
    """Mengambil satu item makanan secara acak berdasarkan list kategori, dan mengeliminasi alergi."""
    query = FoodItem.query.filter(FoodItem.kategori.in_(kategori_list))
    
    if alergi_list:
        # Jika ada alergi, hilangkan makanan yang tags-nya mengandung string alergi tersebut
        for alergi in alergi_list:
            query = query.filter(not_(FoodItem.tags.contains(alergi)))
            
    foods = query.all()
    if foods:
        return random.choice(foods)
    return None

def format_menu_string(items):
    """Menggabungkan list item makanan menjadi string yang rapi dengan kalori."""
    valid_items = [item for item in items if item is not None]
    if not valid_items:
        return "Menu belum tersedia"
    
    names_portions = [f"{item.nama} ({item.porsi})" for item in valid_items]
    total_cal = sum(item.kalori for item in valid_items)
    
    return f"{' + '.join(names_portions)} (~{total_cal} kkal)"

def get_food_recommendations(kalori_harian, alergi_list=None):
    # Proporsi kalori ideal (sebagai referensi matematis)
    sarapan_cal = round(kalori_harian * 0.25)
    siang_cal = round(kalori_harian * 0.35)
    malam_cal = round(kalori_harian * 0.25)
    camilan_cal = round(kalori_harian * 0.15)
    
    # Kategori label
    if kalori_harian < 1500:
        kategori_label = "Rendah Kalori (Defisit)"
    elif 1500 <= kalori_harian <= 2200:
        kategori_label = "Kalori Menengah (Normal)"
    else:
        kategori_label = "Tinggi Kalori (Surplus/Aktivitas Tinggi)"

    # Generate Sarapan (1 Karbo + 1 Lauk (Hewani/Nabati) + opsional sayur/buah)
    sarapan_items = [
        get_random_food(['karbo'], alergi_list),
        get_random_food(['lauk_hewani', 'lauk_nabati'], alergi_list)
    ]
    if random.choice([True, False]):
        sarapan_items.append(get_random_food(['sayuran', 'camilan'], alergi_list))

    # Generate Siang (1 Karbo + 1 Lauk Hewani + 1 Lauk Nabati + 1 Sayur)
    siang_items = [
        get_random_food(['karbo'], alergi_list),
        get_random_food(['lauk_hewani'], alergi_list),
        get_random_food(['lauk_nabati'], alergi_list),
        get_random_food(['sayuran'], alergi_list)
    ]

    # Generate Malam (1 Karbo + 1 Lauk (Hewani/Nabati) + 1 Sayur)
    malam_items = [
        get_random_food(['karbo'], alergi_list),
        get_random_food(['lauk_hewani', 'lauk_nabati'], alergi_list),
        get_random_food(['sayuran'], alergi_list)
    ]

    # Generate Camilan (1 Camilan, tambah 1 jika target kalori tinggi)
    camilan_items = [get_random_food(['camilan'], alergi_list)]
    if kalori_harian > 2000:
        camilan_items.append(get_random_food(['camilan'], alergi_list))

    menu = {
        'sarapan': format_menu_string(sarapan_items),
        'siang': format_menu_string(siang_items),
        'malam': format_menu_string(malam_items),
        'camilan': format_menu_string(camilan_items)
    }
        
    return {
        'kategori': kategori_label,
        'menu': menu,
        'calories': {
            'sarapan': sarapan_cal,
            'siang': siang_cal,
            'malam': malam_cal,
            'camilan': camilan_cal
        }
    }
