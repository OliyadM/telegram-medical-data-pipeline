import os
import json
from ultralytics import YOLO

# Path to the folder containing images
IMAGES_ROOT = 'data/raw/telegram_images'

# Output detection results file
OUTPUT_FILE = 'enrichment/detections.json'

def find_images(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                yield os.path.join(dirpath, filename)

def extract_message_id_from_path(path):
    filename = os.path.basename(path)
    name_without_ext = os.path.splitext(filename)[0]  # "10" or "18525_abc"

    # If underscore exists, take part before underscore, else take entire name_without_ext
    if '_' in name_without_ext:
        message_id_part = name_without_ext.split('_')[0]
    else:
        message_id_part = name_without_ext

    return int(message_id_part)


def main():
    model = YOLO('yolov8n.pt')  # You can choose a bigger model for better accuracy if you want

    detection_results = []

    for image_path in find_images(IMAGES_ROOT):
        message_id = extract_message_id_from_path(image_path)

        results = model(image_path)[0]  # Run inference on image

        for result in results.boxes.data.tolist():
            # result format: [x1, y1, x2, y2, confidence, class]
            confidence = result[4]
            class_id = int(result[5])
            detected_class = model.names[class_id]

            detection_results.append({
                'message_id': message_id,
                'image_path': image_path,
                'detected_class': detected_class,
                'confidence': confidence
            })

    # Save to JSON
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(detection_results, f, indent=2)

    print(f'Detection complete. Results saved to {OUTPUT_FILE}')

if __name__ == '__main__':
    main()
