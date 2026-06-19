# Base outputs for Sugeno (Constants for defuzzification)
# This table is generated to cover all 36 combinations (4 BMI x 3 Aktivitas x 3 Umur)
RULES = [
    # (bmi, aktivitas, umur, output_kalori)
    
    # Underweight
    ('underweight', 'rendah', 'muda', 2000),
    ('underweight', 'rendah', 'dewasa', 1900),
    ('underweight', 'rendah', 'senior', 1800),
    
    ('underweight', 'sedang', 'muda', 2300),
    ('underweight', 'sedang', 'dewasa', 2200),
    ('underweight', 'sedang', 'senior', 2000),
    
    ('underweight', 'tinggi', 'muda', 2700),
    ('underweight', 'tinggi', 'dewasa', 2600),
    ('underweight', 'tinggi', 'senior', 2400),
    
    # Normal
    ('normal', 'rendah', 'muda', 1900),
    ('normal', 'rendah', 'dewasa', 1800),
    ('normal', 'rendah', 'senior', 1700),
    
    ('normal', 'sedang', 'muda', 2200),
    ('normal', 'sedang', 'dewasa', 2100),
    ('normal', 'sedang', 'senior', 1900),
    
    ('normal', 'tinggi', 'muda', 2600),
    ('normal', 'tinggi', 'dewasa', 2500),
    ('normal', 'tinggi', 'senior', 2300),
    
    # Overweight (Aimed at deficit)
    ('overweight', 'rendah', 'muda', 1600),
    ('overweight', 'rendah', 'dewasa', 1500),
    ('overweight', 'rendah', 'senior', 1400),
    
    ('overweight', 'sedang', 'muda', 1900),
    ('overweight', 'sedang', 'dewasa', 1800),
    ('overweight', 'sedang', 'senior', 1700),
    
    ('overweight', 'tinggi', 'muda', 2300),
    ('overweight', 'tinggi', 'dewasa', 2200),
    ('overweight', 'tinggi', 'senior', 2000),
    
    # Obese (More aggressive deficit)
    ('obese', 'rendah', 'muda', 1400),
    ('obese', 'rendah', 'dewasa', 1300),
    ('obese', 'rendah', 'senior', 1200),
    
    ('obese', 'sedang', 'muda', 1700),
    ('obese', 'sedang', 'dewasa', 1600),
    ('obese', 'sedang', 'senior', 1500),
    
    ('obese', 'tinggi', 'muda', 2000),
    ('obese', 'tinggi', 'dewasa', 1900),
    ('obese', 'tinggi', 'senior', 1800),
]
