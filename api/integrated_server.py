import os
import cv2
import json
import logging
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from threading import Lock
from ultralytics import YOLO
import sys

# Add parent directory to path so risk_engine can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from risk_engine.risk_rules import get_behavior_score

app = FastAPI(title="XYRA Sentinel API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO("yolov8n.pt")
camera = cv2.VideoCapture(0)
lock = Lock()

latest_metrics = {
    "num_people": 0,
    "risk_level": "LOW",
    "score": 0.0,
    "status": "Normal"
}

def generate_frames():
    global latest_metrics
    import numpy as np
    while True:
        success, frame = camera.read()
        if not success:
            # Fallback black frame if no camera is available
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "WAITING FOR CAMERA", (100, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            results = None
            annotated_frame = frame
        else:
            # Run inference
            results = model(frame, verbose=False)
            annotated_frame = results[0].plot()
        
        # Calculate true risk from detections
        boxes = results[0].boxes if results else None
        risk_data = get_behavior_score(boxes)
        
        # Update metrics thread-safely
        with lock:
            if boxes is not None:
                latest_metrics["num_people"] = len([b for b in boxes if int(b.cls[0]) == 0])
            else:
                latest_metrics["num_people"] = 0
            latest_metrics["risk_level"] = risk_data["level"]
            latest_metrics["score"] = risk_data["score"]
            latest_metrics["status"] = "Threat" if risk_data["level"] == "HIGH" else "Normal"

        _, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

from fastapi.staticfiles import StaticFiles

# ... Mount the frontend static files ...
# Note: we need to place this at the end or change the route. Actually, mounting at "/" covers the root.
# Let's adjust the imports and mount.

# Define API routes under /api/
@app.get("/api/metrics")
def get_metrics():
    with lock:
        return latest_metrics

@app.get("/api/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

# Mount static frontend
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.on_event("shutdown")
def shutdown_event():
    camera.release()

