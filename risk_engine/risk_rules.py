import random

def get_behavior_score():
    return random.uniform(0, 1)

def calculate_risk(score):
    if score > 0.8:
        return "HIGH"
    elif score > 0.5:
        return "MEDIUM"
    else:
        return "LOW"
