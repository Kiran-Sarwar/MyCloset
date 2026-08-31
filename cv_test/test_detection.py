from ultralytics import YOLO

# Load a small pretrained YOLO model
model = YOLO("yolo11n.pt")

# Run detection on the test clothing image
results = model("cv_test/jeans.jpg")

# Display detected objects
for result in results:
    print("\nDetected objects:")

    if result.boxes is None or len(result.boxes) == 0:
        print("No objects detected.")
        continue

    for box in result.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = result.names[class_id]

        print(
            f"- {class_name} "
            f"(confidence: {confidence:.2f})"
        )