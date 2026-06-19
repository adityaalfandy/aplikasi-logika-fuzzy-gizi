import pytest
from app.fuzzy.engine import FuzzySugenoEngine

@pytest.fixture
def engine():
    return FuzzySugenoEngine()

from app.fuzzy.membership import Membership

def test_membership_bmi(engine):
    # BMI = 22 (Normal)
    mu = Membership.bmi(22)
    assert mu.get('underweight', 0) == 0.0
    assert mu.get('normal', 0) > 0.0

    # BMI = 17 (Underweight)
    mu = Membership.bmi(17)
    assert mu.get('underweight', 0) > 0.0
    assert mu.get('normal', 0) == 0.0

    # BMI = 28 (Overweight)
    mu = Membership.bmi(28)
    assert mu.get('overweight', 0) > 0
    assert mu.get('normal', 0) == 0

def test_fuzzy_calculation(engine):
    # Laki-laki, berat 70kg, tinggi 175cm -> BMI = 22.86 (Normal)
    # Umur 25 (Muda)
    # Aktivitas Moderately (1.55)
    
    result = engine.calculate(bmi_val=22.86, aktivitas_val=1.55, umur_val=25)
    
    assert 'kalori_fuzzy' in result
    assert result['kalori_fuzzy'] > 0
    
    # Test kalori_fuzzy is an integer
    assert isinstance(result['kalori_fuzzy'], int)
    
    # Assert Z falls within expected human bounds (e.g. 1500 to 4000)
    assert 1500 <= result['kalori_fuzzy'] <= 4000

def test_extreme_cases(engine):
    # Extremely low values
    result_low = engine.calculate(bmi_val=10, aktivitas_val=1.2, umur_val=10)
    assert result_low['kalori_fuzzy'] > 0

    # Extremely high values
    result_high = engine.calculate(bmi_val=50, aktivitas_val=1.9, umur_val=90)
    assert result_high['kalori_fuzzy'] > 0
