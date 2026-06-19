from app.fuzzy.membership import Membership
from app.fuzzy.rules import RULES
from app.fuzzy.defuzzification import weighted_average

class FuzzySugenoEngine:
    def __init__(self):
        self.rules = RULES

    def calculate(self, bmi_val, aktivitas_val, umur_val):
        # 1. Fuzzification (Calculate Memberships)
        mem_bmi = Membership.bmi(bmi_val)
        mem_aktivitas = Membership.aktivitas(aktivitas_val)
        mem_umur = Membership.umur(umur_val)

        # 2. Inference (Rule Evaluation)
        fired_rules = []
        rule_id = 1
        for rule_bmi, rule_akt, rule_umur, output_kalori in self.rules:
            # AND operator uses MIN
            weight = min(
                mem_bmi.get(rule_bmi, 0),
                mem_aktivitas.get(rule_akt, 0),
                mem_umur.get(rule_umur, 0)
            )
            
            if weight > 0:
                fired_rules.append({
                    'id': rule_id,
                    'desc': f"IF BMI is {rule_bmi.title()} AND Aktivitas is {rule_akt.title()} AND Umur is {rule_umur.title()} THEN Kalori = {output_kalori}",
                    'weight': round(weight, 4),
                    'output': output_kalori
                })
            rule_id += 1

        # 3. Defuzzification
        kalori_fuzzy = weighted_average(fired_rules)

        # Format output for XAI
        defuzz_steps = ""
        if fired_rules:
            num_str = " + ".join([f"({r['weight']}×{r['output']})" for r in fired_rules])
            den_str = " + ".join([str(r['weight']) for r in fired_rules])
            defuzz_steps = f"({num_str}) / ({den_str}) = {kalori_fuzzy} kkal"
        else:
            defuzz_steps = "0 / 0 = 0 kkal"

        return {
            'kalori_fuzzy': kalori_fuzzy,
            'membership': {
                'bmi': {k: round(v, 4) for k, v in mem_bmi.items() if v > 0},
                'aktivitas': {k: round(v, 4) for k, v in mem_aktivitas.items() if v > 0},
                'umur': {k: round(v, 4) for k, v in mem_umur.items() if v > 0}
            },
            'fired_rules': fired_rules,
            'defuzz_steps': defuzz_steps
        }
