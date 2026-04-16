# XYRA Sentinel 🛡️

**XYRA Sentinel** is an AI-powered, real-time retail surveillance and intelligence system. It utilizes advanced deep learning (YOLOv8 & PyTorch) to proactively monitor camera feeds, detect individuals, and evaluate real-time behavioral risk scores to identify potential shoplifting or suspicious activities in a retail environment.

It features a stunning **3D-enabled dashboard** that brings real-time analytics to life, overlaying bounding boxes, tracking individuals, and displaying dynamic risk metrics in a robust web interface. 

---

## 🌟 Core Features

- **Real-Time Object Detection**: Powerful, low-latency tracking of people and movements using custom-tailored YOLOv8 model inference.
- **Dynamic Risk Engine**: Evaluates bounding box intersections, crowd density, and individual behaviors to calculate a normalized risk score ("LOW", "MEDIUM", "HIGH").
- **3D Retail Dashboard**: Built using modern vanilla CSS and JavaScript with Three.js (via pathways/WebGL) to visualize store environments, tracking retail floor telemetry dynamically.
- **Unified API Server**: A high-performance FastAPI backend that streams WebRTC/Multipart video grids directly to the browser alongside JSON metric endpoints.
- **Threat Event Logging**: Automatically flags "Threat" status when risk calculations exceed predefined risk thresholds.

---

## 🏗️ Architecture & Tech Stack

- **Backend**: Python 3, FastAPI, Uvicorn (Asynchronous REST API & Video Streaming)
- **AI/ML**: PyTorch, Ultralytics YOLOv8, OpenCV (Computer Vision and Tensor-based inference)
- **Frontend**: HTML5, Vanilla JavaScript, CSS3 (Glassmorphism UI, Responsive Grid)
- **Data Pipeline**: Custom scripts for stream input (`stream_input/`), tracking (`tracking/`), and database integrations (`database/`).

---

## 📁 Repository Structure

```text
├── api/                   # FastAPI integrated server endpoints
├── frontend/              # 3D-enabled dashboard (HTML, JS, CSS)
├── risk_engine/           # Algorithms for real-time behavior scoring
├── tracking/              # DeepSORT/ByteTrack implementation (if applicable)
├── dashboard.py           # Legacy Streamlit interactive dashboard
├── main.py                # Core Python pipeline
├── start.sh               # Initialization script for the application
├── yolov8n.pt             # Tiny YOLOv8 model weights
└── requirements.txt       # Python dependencies
```

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.9+ installed and a working webcam connected to your system.

### 2. Installation
Clone the repository and install the dependencies in a virtual environment:
```bash
git clone https://github.com/natanshsingh/XYRA-Sentinel.git
cd XYRA-Sentinel

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Running the System

You can boot up the entire backend API and 3D frontend using the startup script:

```bash
chmod +x start.sh
./start.sh
```

**What this does:**
1. Loads the YOLOv8 model weights locally.
2. Initializes the `cv2.VideoCapture` thread to pull hardware camera feeds.
3. Serves the REST API and the static 3D Dashboard simultaneously.

Once running, open your browser and navigate to: **`http://localhost:8000`**

---

## 🔌 API Endpoints

The backend exposes a few lightweight endpoints for seamless integration:

- `GET /api/video_feed`: Returns a `multipart/x-mixed-replace` continuous motion JPEG (MJPEG) stream containing the camera feed rendered with YOLO bounding boxes.
- `GET /api/metrics`: Returns a real-time JSON payload containing current surveillance metrics.
    ```json
    {
        "num_people": 4,
        "risk_level": "MEDIUM",
        "score": 45.2,
        "status": "Normal"
    }
    ```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
