import os
import shutil
import random

SOURCE = "dataset"  
TRAIN = "data/train"
VAL = "data/val"
SPLIT_RATIO = 0.8

for category in ["shoplifting", "normal"]:
    source_dir = os.path.join(SOURCE, category)
    train_dir = os.path.join(TRAIN, category)
    val_dir = os.path.join(VAL, category)

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    images = os.listdir(source_dir)
    random.shuffle(images)

    split_index = int(len(images) * SPLIT_RATIO)

    for img in images[:split_index]:
        shutil.copy(os.path.join(source_dir, img), train_dir)

    for img in images[split_index:]:
        shutil.copy(os.path.join(source_dir, img), val_dir)

print("Data split complete.")
