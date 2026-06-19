def trimf(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)
    return 0.0

def trapmf(x, a, b, c, d):
    if x <= a or x >= d:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a) if b != a else 1.0
    elif b < x <= c:
        return 1.0
    elif c < x < d:
        return (d - x) / (d - c) if d != c else 1.0
    return 0.0

class Membership:
    @staticmethod
    def bmi(val):
        return {
            'underweight': trapmf(val, 0, 0, 17, 18.5),
            'normal': trapmf(val, 17.5, 18.5, 24.9, 25.5),
            'overweight': trapmf(val, 24.5, 25.0, 29.9, 30.5),
            'obese': trapmf(val, 29.5, 30.0, 60, 60)
        }

    @staticmethod
    def aktivitas(val):
        return {
            'rendah': trapmf(val, 1.0, 1.0, 1.2, 1.375),
            'sedang': trimf(val, 1.2, 1.375, 1.55),
            'tinggi': trapmf(val, 1.375, 1.55, 2.0, 2.0)
        }

    @staticmethod
    def umur(val):
        return {
            'muda': trapmf(val, 0, 0, 20, 25),
            'dewasa': trimf(val, 20, 32.5, 45),
            'senior': trapmf(val, 40, 45, 100, 100)
        }
