import pathway as pw
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import resnet18
from PIL import Image
import io
import os
import logging


ALERT_THRESHOLD = 80  


os.makedirs("output_stream", exist_ok=True)

logging.basicConfig(
    filename="output_stream/system.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

def log_event(message: str):
    print(message)  
    logging.info(message)


device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

model = resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, 2)

model.load_state_dict(
    torch.load("models/saved_models/behavior_model.pt", map_location=device)
)

model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

images = pw.io.fs.read(
    "stream_input",
    format="binary"
)

@pw.udf
def classify_image(image_bytes: bytes):

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img)
        probabilities = torch.softmax(output, dim=1)
        confidence, prediction = torch.max(probabilities, dim=1)

    confidence_score = round(float(confidence.item() * 100), 2)
    label = "🚨 SHOPLIFTING" if prediction.item() == 1 else "Normal"

    
    if label == "🚨 SHOPLIFTING" and confidence_score >= ALERT_THRESHOLD:
        alert_message = f"🚨 ALERT: Shoplifting detected | Confidence: {confidence_score}%"
        log_event(alert_message)

    return label, confidence_score


results = images.select(
    prediction=classify_image(pw.this.data)
)

results = results.select(
    label=pw.this.prediction[0],
    confidence=pw.this.prediction[1],
)

pw.io.csv.write(
    results,
    "output_stream/results.csv"
)

log_event("🚀 AI Surveillance System Started...")
pw.run()