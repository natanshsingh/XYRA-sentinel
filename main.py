from ultralytics import YOLO
import cv2
from risk_engine.risk_rules import calculate_risk, get_behavior_score

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Object detection
    results = model(frame)
    annotated = results[0].plot()


    score = get_behavior_score()
    risk = calculate_risk(score)

    cv2.putText(
        annotated,
        f"Risk Level: {risk}",
        (40, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    cv2.imshow("Retail AI Monitoring", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
