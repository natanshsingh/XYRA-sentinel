import os
import random
import shutil

NORMAL_SRC = r"C:\Hackaton 2\data\train\normal"
SHOP_SRC = r"C:\Hackaton 2\data\train\shoplifting"

BASE_DST = r"C:\Hackaton 2\data_sampled"

TRAIN_RATIO = 0.8          
SAMPLES_PER_CLASS = 7000   

def prepare_class(src, class_name):
    images = [
        f for f in os.listdir(src)
        if f.lower().endswith(('.jpg', '.png', '.jpeg'))
    ]

    random.shuffle(images)
    images = images[:SAMPLES_PER_CLASS]

    split_idx = int(len(images) * TRAIN_RATIO)
    train_imgs = images[:split_idx]
    val_imgs = images[split_idx:]

    train_dir = os.path.join(BASE_DST, "train", class_name)
    val_dir = os.path.join(BASE_DST, "val", class_name)

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    for img in train_imgs:
        shutil.copy(os.path.join(src, img), train_dir)

    for img in val_imgs:
        shutil.copy(os.path.join(src, img), val_dir)

    print(f"{class_name}: {len(train_imgs)} train, {len(val_imgs)} val")

print("🚀 Sampling dataset...")

prepare_class(NORMAL_SRC, "normal")
prepare_class(SHOP_SRC, "shoplifting")

print("✅ Dataset sampling complete")
