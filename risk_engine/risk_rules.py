def calculate_risk(num_people: int, suspicious_behaviors: int = 0) -> dict:
    """
    Calculate real risk based on the number of people and any flagged behaviors.
    Returns a dict with risk_level ("LOW", "MEDIUM", "HIGH") and raw score.
    """
    score = (num_people * 0.1) + (suspicious_behaviors * 0.4)
    # cap at 1.0
    score = min(score, 1.0)
    
    if score > 0.8:
        level = "HIGH"
    elif score > 0.4:
        level = "MEDIUM"
    else:
        level = "LOW"
        
    return {
        "score": round(score, 2),
        "level": level
    }

def get_behavior_score(boxes):
    """
    Parses YOLO detections for behavior estimation.
    """
    num_people = 0
    suspicious = 0
    # YOLO typically outputs class 0 for 'person'
    if boxes is not None:
        for box in boxes:
            if int(box.cls[0]) == 0:
                num_people += 1
            
    return calculate_risk(num_people, suspicious_behaviors=suspicious)

