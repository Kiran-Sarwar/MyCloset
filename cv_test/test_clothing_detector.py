import sys
from pathlib import Path

# Add the MyCloset project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.clothing_detector import detect_clothing


test_images = [
    "cv_test/jeans_test.jpg",
    "cv_test/shirt.jpg",
    "cv_test/one-piece_test.jpg",
    "cv_test/outerwear_test.jpg",
]


for image_path in test_images:

    print(f"\n{'=' * 50}")
    print(f"Testing: {image_path}")
    print(f"{'=' * 50}")

    detections = detect_clothing(image_path)

    if not detections:
        print("No clothing items detected.")
        continue

    for detection in detections:
        print(
            f"- Category: {detection['category']}"
            f" | Model label: {detection['model_label']}"
            f" | Confidence: {detection['confidence']}"
        )