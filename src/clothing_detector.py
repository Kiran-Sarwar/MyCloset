from pathlib import Path

from ultralytics import YOLO


# Path to the DeepFashion2 model
MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "deepfashion2_yolov8s-seg.pt"
)


# Minimum confidence required for a detection
CONFIDENCE_THRESHOLD = 0.50


# Confidence level considered safe for automatic acceptance
AUTO_ACCEPT_CONFIDENCE = 0.70


# IoU threshold used to identify overlapping duplicate detections
DUPLICATE_IOU_THRESHOLD = 0.50


# DeepFashion2 labels → MyCloset categories
CATEGORY_MAPPING = {
    "short_sleeved_shirt": "shirt",
    "long_sleeved_shirt": "shirt",
    "short_sleeved_outwear": "outerwear",
    "long_sleeved_outwear": "outerwear",
    "trousers": "pants",
    "skirt": "skirt",
    "short_sleeved_dress": "dress",
    "long_sleeved_dress": "dress",
    "sling_dress": "dress",
    "vest_dress": "dress",
    "vest": "vest",
    "shorts": "shorts",
}


# DeepFashion2 labels → user-friendly clothing names
DISPLAY_NAME_MAPPING = {
    "short_sleeved_shirt": "Short-Sleeve Shirt",
    "long_sleeved_shirt": "Long-Sleeve Shirt",
    "short_sleeved_outwear": "Short-Sleeve Outerwear",
    "long_sleeved_outwear": "Long-Sleeve Outerwear",
    "trousers": "Trousers",
    "skirt": "Skirt",
    "short_sleeved_dress": "Short-Sleeve Dress",
    "long_sleeved_dress": "Long-Sleeve Dress",
    "sling_dress": "Sling Dress",
    "vest_dress": "Vest Dress",
    "vest": "Vest",
    "shorts": "Shorts",
}


# Load the model once
model = YOLO(str(MODEL_PATH))


def calculate_iou(box_a, box_b):
    """
    Calculate Intersection over Union (IoU)
    between two bounding boxes.

    Each box is in the format:
    [x1, y1, x2, y2]
    """

    x1 = max(box_a[0], box_b[0])
    y1 = max(box_a[1], box_b[1])
    x2 = min(box_a[2], box_b[2])
    y2 = min(box_a[3], box_b[3])

    intersection_width = max(0, x2 - x1)
    intersection_height = max(0, y2 - y1)

    intersection_area = (
        intersection_width * intersection_height
    )

    area_a = (
        max(0, box_a[2] - box_a[0])
        * max(0, box_a[3] - box_a[1])
    )

    area_b = (
        max(0, box_b[2] - box_b[0])
        * max(0, box_b[3] - box_b[1])
    )

    union_area = area_a + area_b - intersection_area

    if union_area == 0:
        return 0.0

    return intersection_area / union_area


def remove_duplicate_detections(detections):
    """
    Remove overlapping detections that represent
    the same MyCloset category.

    When two detections overlap heavily, the detection
    with the higher confidence is kept.
    """

    detections = sorted(
        detections,
        key=lambda item: item["confidence"],
        reverse=True,
    )

    kept_detections = []

    for detection in detections:

        is_duplicate = False

        for kept in kept_detections:

            if detection["category"] != kept["category"]:
                continue

            iou = calculate_iou(
                detection["box"],
                kept["box"],
            )

            if iou >= DUPLICATE_IOU_THRESHOLD:
                is_duplicate = True
                break

        if not is_duplicate:
            kept_detections.append(detection)

    return kept_detections


def detect_clothing(image_path):
    """
    Detect clothing items in an image.

    Returns a list of dictionaries containing:
    - MyCloset category
    - original model label
    - user-friendly display name
    - confidence
    - confidence status
    - bounding box
    """

    results = model(image_path)

    detections = []

    for result in results:

        if result.boxes is None or len(result.boxes) == 0:
            continue

        for box in result.boxes:

            confidence = float(box.conf[0])

            if confidence < CONFIDENCE_THRESHOLD:
                continue

            class_id = int(box.cls[0])

            model_label = result.names[class_id]

            category = CATEGORY_MAPPING.get(
                model_label
            )

            if category is None:
                continue

            display_name = DISPLAY_NAME_MAPPING.get(
                model_label,
                model_label.replace("_", " ").title(),
            )

            if confidence >= AUTO_ACCEPT_CONFIDENCE:
                confidence_status = "high"
            else:
                confidence_status = "review"

            coordinates = box.xyxy[0].tolist()

            detections.append(
                {
                    "category": category,
                    "model_label": model_label,
                    "display_name": display_name,
                    "confidence": round(confidence, 2),
                    "confidence_status": confidence_status,
                    "box": coordinates,
                }
            )

    detections = remove_duplicate_detections(
        detections
    )

    return detections