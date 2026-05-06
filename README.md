# 🛡️ XYRA Sentinel

**XYRA Sentinel** is an AI-powered, real-time retail surveillance and intelligence system designed to proactively detect suspicious behavior and potential theft in physical environments using computer vision and intelligent risk scoring.

Retail businesses face significant losses due to undetected theft and inefficient monitoring. XYRA Sentinel addresses this by combining **real-time object detection**, **behavioral analysis**, and an **interactive visualization dashboard** to deliver actionable insights for smarter, automated security.

---

## 🚨 Overview

Traditional surveillance systems are passive—they record events but do not actively interpret them.

**XYRA Sentinel transforms surveillance into an intelligent system** by:
- Continuously monitoring live camera feeds  
- Detecting individuals and tracking movement patterns  
- Evaluating behavioral risk in real time  
- Flagging potential threats before incidents escalate  

---

## 🌟 Core Features

- **Real-Time Object Detection**  
  High-performance detection and tracking of individuals using a YOLOv8-based pipeline optimized for low-latency inference.

- **Dynamic Risk Engine**  
  Computes real-time risk scores based on:
  - Proximity to sensitive or restricted zones  
  - Sudden or unusual movement patterns  
  - Crowd density and clustering behavior  

- **Threat Detection System**  
  Automatically flags high-risk individuals when predefined thresholds are exceeded, enabling proactive intervention.

- **Interactive 3D Dashboard**  
  A browser-based visualization layer that:
  - Displays live bounding boxes and tracking  
  - Renders dynamic metrics in real time  
  - Provides an intuitive monitoring interface  

- **Unified API Backend**  
  FastAPI-powered backend serving:
  - Live video streams (MJPEG)  
  - Real-time analytics and metrics via REST endpoints  

- **Event Logging & Monitoring**  
  Logs system events and threat detections for further analysis and auditing.

---

## 🏗️ Architecture & Tech Stack

### Backend
- Python 3  
- FastAPI  
- Uvicorn  

### AI / ML
- PyTorch  
- Ultralytics YOLOv8  
- OpenCV  

### Frontend
- HTML5  
- Vanilla JavaScript  
- CSS3  
- WebGL / Three.js  

### System Components
- Real-time video ingestion pipeline  
- Object detection + tracking layer  
- Risk scoring engine  
- API server + dashboard interface  

---

## 🖼️ Demo & Screenshots

### Real-Time Detection
![Detection Output](./assets/detection.png)

### Risk Monitoring Dashboard
![Dashboard](./assets/dashboard.png)

### Tracking & Analytics
![Tracking](./assets/tracking.png)

---

## 💡 Use Cases

- Retail theft detection and prevention  
- Smart store surveillance systems  
- Crowd behavior analysis in public environments  
- Automated security monitoring for physical spaces  

---

## 📁 Repository Structure

├── api/                   # FastAPI server endpoints  
├── frontend/              # Dashboard (HTML, JS, CSS)  
├── risk_engine/           # Risk scoring algorithms  
├── tracking/              # Object tracking (DeepSORT/ByteTrack)  
├── dashboard.py           # Streamlit dashboard (legacy)  
├── main.py                # Core pipeline  
├── start.sh               # Startup script  
├── yolov8n.pt             # Model weights  
└── requirements.txt       # Dependencies  

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+  
- Webcam or video input source  

### 2. Installation

git clone https://github.com/natanshsingh/XYRA-Sentinel.git  
cd XYRA-Sentinel  

python3 -m venv venv  
source venv/bin/activate  

pip install -r requirements.txt  

---

### 3. Run the System

chmod +x start.sh  
./start.sh  

### What Happens:
- YOLOv8 model loads locally  
- Video stream initializes  
- Backend API starts  
- Dashboard becomes available  

Open in browser:  
http://localhost:8000  

---

## 🔌 API Endpoints

### GET /api/video_feed
Returns a continuous MJPEG stream with bounding box overlays.

### GET /api/metrics
Returns real-time system metrics:

{
  "num_people": 4,
  "risk_level": "MEDIUM",
  "score": 45.2,
  "status": "Normal"
}

---

## 🚀 Future Improvements

- Multi-camera synchronization and tracking  
- Cloud-based deployment support  
- Advanced anomaly detection using sequence models  
- Real-time alert system (SMS/Email)  

---
<img width="823" height="487" alt="Screenshot 2026-05-06 at 5 37 29 PM" src="https://github.com/user-attachments/assets/62d523aa-1ecb-4209-8361-0ffb5df3346d" />
## 📄 License

This project is licensed under the MIT License.
