# Phase 3D — Computer Vision Integration

**Status:** Complete
**Project:** MyCloset
**Phase:** 3D

---

## 1. Goal

The goal of Phase 3D was to introduce computer vision into MyCloset so the application could automatically identify clothing items from uploaded images.

Instead of requiring the user to manually select the clothing type and category, MyCloset can now analyze an uploaded image and suggest the appropriate clothing information.

---

## 2. Computer Vision Model

MyCloset uses a **DeepFashion2-trained YOLO model**:

```text
deepfashion2_yolov8s-seg.pt
```

The model is used to detect clothing items in uploaded images.

The model was selected because a general-purpose YOLO model did not reliably recognize clothing. For example, the generic YOLO11n model incorrectly identified a jeans image as a tie.

DeepFashion2 produced significantly better clothing-specific results.

---

## 3. Detection Pipeline

The current computer vision workflow is:

```text
User uploads image
        ↓
Flask receives image
        ↓
Image is temporarily saved
        ↓
DeepFashion2 model analyzes image
        ↓
Clothing item is detected
        ↓
Model label is mapped to MyCloset category
        ↓
User-friendly clothing name is generated
        ↓
Confidence is evaluated
        ↓
Result is returned to the interface
```

When the item is finally added, the image is saved permanently in:

```text
src/static/uploads/
```

---

## 4. Clothing Category Mapping

DeepFashion2 model labels are converted into MyCloset's existing categories.

| Model Label           | MyCloset Category |
| --------------------- | ----------------- |
| short_sleeved_shirt   | Tops              |
| long_sleeved_shirt    | Tops              |
| vest                  | Tops              |
| trousers              | Bottoms           |
| skirt                 | Bottoms           |
| shorts                | Bottoms           |
| short_sleeved_dress   | One-Piece         |
| long_sleeved_dress    | One-Piece         |
| sling_dress           | One-Piece         |
| vest_dress            | One-Piece         |
| short_sleeved_outwear | Outerwear         |
| long_sleeved_outwear  | Outerwear         |

This allows the computer vision system to work with the categories already used by the MyCloset application.

---

## 5. User-Friendly Clothing Names

Raw model labels are not displayed directly to the user.

For example:

```text
short_sleeved_shirt
```

is displayed as:

```text
Short-Sleeve Shirt
```

Other examples include:

```text
trousers → Trousers
sling_dress → Sling Dress
long_sleeved_outwear → Long-Sleeve Outerwear
```

This keeps the interface understandable while preserving the original model labels internally.

---

## 6. Confidence Handling

The detector uses two confidence levels.

### Minimum Detection Threshold

```text
0.50
```

Detections below 50% confidence are ignored.

### Automatic Acceptance Threshold

```text
0.70
```

A detection with 70% or higher confidence is considered high-confidence.

Detections between 50% and 69% are marked for review.

Example:

```text
Detected: Short-Sleeve Shirt (93% confidence)
```

For a lower-confidence result:

```text
Detected: Short-Sleeve Shirt (61% confidence) — Please review.
```

This prevents the system from treating uncertain predictions as completely reliable.

---

## 7. Duplicate Detection Handling

Multiple overlapping detections of the same clothing category can occur.

MyCloset uses **Intersection over Union (IoU)** to identify heavily overlapping duplicate detections.

Current duplicate threshold:

```text
0.50
```

When two detections of the same category overlap significantly, the detection with the higher confidence is kept.

Different categories are allowed to remain.

For example, an image can correctly produce:

```text
Long-Sleeve Outerwear
Trousers
```

while duplicate detections of the same item are removed.

---

## 8. Flask Integration

A new `/detect` endpoint was added to the Flask application.

The endpoint:

1. Receives an uploaded image.
2. Validates the file type.
3. Temporarily saves the image.
4. Runs computer vision detection.
5. Converts the result to a MyCloset category.
6. Returns the detected clothing type and confidence.
7. Deletes the temporary image.

The frontend communicates with this endpoint using JavaScript `fetch()`.

---

## 9. Add Item Integration

Computer vision is also integrated into the normal **Add Clothing Item** workflow.

When an image is uploaded:

```text
Image
 ↓
Detection
 ↓
Detected category/type
 ↓
Form automatically updated
 ↓
User reviews information
 ↓
Add to MyCloset
```

When the item is submitted, the uploaded image is stored permanently and the detected category/type is used when available.

The existing manual selection system remains available as a fallback.

---

## 10. Image Upload Handling

MyCloset currently supports:

```text
.jpg
.jpeg
.png
.gif
.webp
```

Maximum upload size:

```text
5 MB
```

Uploaded filenames are secured using `secure_filename()` and unique filenames are generated using UUIDs.

This prevents filename collisions and keeps uploaded files separated from the original filenames.

---

## 11. Testing

The computer vision system was tested using multiple clothing images.

### Test Results

| Image                | Expected Detection               | Result   |
| -------------------- | -------------------------------- | -------- |
| `jeans_test.jpg`     | Trousers                         | ✅ Passed |
| `shirt.jpg`          | Short-Sleeve Shirt               | ✅ Passed |
| `one-piece_test.jpg` | Dress                            | ✅ Passed |
| `outerwear_test.jpg` | Outerwear + Trousers             | ✅ Passed |
| Non-clothing image   | No clothing detection / fallback | ✅ Passed |

Example detection results included:

```text
Trousers — 92%
Short-Sleeve Shirt — 93%
Sling Dress — 81%
Long-Sleeve Outerwear — 90%
```

The system was also tested through the actual Flask interface to verify that detection results were correctly transferred into the Add Clothing form and saved to the wardrobe.

---

## 12. Files Added or Updated

The main files involved in Phase 3D include:

```text
deepfashion2_yolov8s-seg.pt
src/clothing_detector.py
src/wardrobe_manager.py
src/app.py
src/templates/add_item.html
cv_test/test_detection.py
```

The upload directory is:

```text
src/static/uploads/
```

---

## 13. Current Limitations

The computer vision system is functional but is still an MVP-level implementation.

Current limitations include:

* Detection accuracy depends on the image quality and clothing visibility.
* The model does not identify every possible clothing type.
* Colors are not automatically detected yet.
* Season is not automatically detected.
* Occasion is not automatically detected.
* Shoes and accessories are not currently part of the DeepFashion2 mapping.
* The system currently selects the highest-confidence detection as the main item during the Add workflow.
* The image is analyzed once during preview and again when the item is submitted.

These limitations can be addressed in future phases.

---

## 14. Phase 3D Outcome

Phase 3D successfully introduced computer vision into MyCloset.

The application can now:

* Accept clothing images.
* Detect clothing using a clothing-specific AI model.
* Convert model predictions into MyCloset categories.
* Display user-friendly clothing names.
* Show detection confidence.
* Warn users about lower-confidence predictions.
* Remove duplicate detections.
* Automatically populate clothing category and type.
* Save uploaded clothing images.
* Fall back to manual selection when detection fails.

---

## 15. Completion Status

### Phase 3D — COMPLETE 

The computer vision foundation is now ready for future AI functionality.

The next stages can build on this foundation to make MyCloset more intelligent, particularly by expanding clothing understanding and eventually generating personalized outfit recommendations.
