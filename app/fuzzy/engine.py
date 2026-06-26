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
            mu_b = mem_bmi.get(rule_bmi, 0)
            mu_a = mem_aktivitas.get(rule_akt, 0)
            mu_u = mem_umur.get(rule_umur, 0)
            
            # AND operator uses MIN
            weight = min(mu_b, mu_a, mu_u)
            
            if weight > 0:
                fired_rules.append({
                    'id': rule_id,
                    'desc': f"IF BMI is {rule_bmi.title()} AND Aktivitas is {rule_akt.title()} AND Umur is {rule_umur.title()} THEN Kalori = {output_kalori}",
                    'weight': round(weight, 4),
                    'output': output_kalori,
                    'calc_alpha': f"min({round(mu_b, 4)}, {round(mu_a, 4)}, {round(mu_u, 4)})"
                })
            rule_id += 1

        # 3. Defuzzification
        kalori_fuzzy = weighted_average(fired_rules)

        # Format output for XAI
        num_str = ""
        den_str = ""
        defuzz_steps = ""
        if fired_rules:
            num_str = " + ".join([f"({r['weight']} \\cdot {r['output']})" for r in fired_rules])
            den_str = " + ".join([str(r['weight']) for r in fired_rules])
            defuzz_steps = f"\\frac{{{num_str}}}{{{den_str}}} = {kalori_fuzzy}"
        else:
            defuzz_steps = "\\frac{0}{0} = 0"

        return {
            'crisp_inputs': {
                'bmi': round(bmi_val, 2),
                'aktivitas': round(aktivitas_val, 3),
                'umur': umur_val
            },
            'kalori_fuzzy': kalori_fuzzy,
            'membership': {
                'bmi': {k: round(v, 4) for k, v in mem_bmi.items()},
                'aktivitas': {k: round(v, 4) for k, v in mem_aktivitas.items()},
                'umur': {k: round(v, 4) for k, v in mem_umur.items()}
            },
            'fired_rules': fired_rules,
            'defuzz_num_str': num_str,
            'defuzz_den_str': den_str,
            'defuzz_steps': defuzz_steps
        }
