def weighted_average(fired_rules):
    """
    Sugeno order-0 defuzzification
    fired_rules: list of dictionaries, e.g. [{'weight': 0.75, 'output': 2400}, ...]
    """
    numerator = sum(rule['weight'] * rule['output'] for rule in fired_rules)
    denominator = sum(rule['weight'] for rule in fired_rules)
    return round(numerator / denominator) if denominator > 0 else 0
