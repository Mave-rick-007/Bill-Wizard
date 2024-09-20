import cv2
import os
from ultralytics import YOLO
from isInvoice import isInvoice


# Load your custom YOLO model
model = YOLO('D:\\billDetection\\Detection-Model\\Detection-Model\\weights\\yolo-v10s.pt')

# Create directory to save captured images if it doesn't exist
output_dir = 'captured_images'
os.makedirs(output_dir, exist_ok=True)

# Open webcam (use 0 for default camera)
cap = cv2.VideoCapture('demoVideos/3.mp4')

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

image_captured = False  # Flag to ensure only one image is captured per object type
image_counter = 0       # Counter for unique image filenames

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Perform YOLO object detection
    results = model(frame)

    # Loop through detected objects (results contains boxes, confidences, class IDs, etc.)
    for result in results:
        # result.boxes contains bounding box information
        boxes = result.boxes
        for box in boxes:
            # Extract bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            # Extract confidence score and class label
            confidence = box.conf[0].item()
            class_id = box.cls[0].item()

            # Get the class name from the model's class names
            class_name = model.names[int(class_id)]

            # Check if the detected object is 'paper' or 'book'
            if (class_name == "paper" or class_name == "book") and confidence > 0.5:
                # Draw green bounding box if it's a "paper" or "book"
                box_color = (0, 255, 0)  # Green
                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)

                # Display label and confidence on the frame
                label_text = f"{class_name} {confidence:.2f}"
                cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                # Ensure a high-resolution image by checking bounding box size
                box_width = x2 - x1
                box_height = y2 - y1
                min_size_threshold = 100  # Set a reasonable size threshold for the object

                if box_width > min_size_threshold and box_height > min_size_threshold and not image_captured:
                    # Capture and save the bounded region
                    cropped_image = frame[y1:y2, x1:x2]  # Crop the region inside the bounding box

                    # Create a unique filename and save the image in the directory
                    image_filename = f'{class_name}_{image_counter}.png'
                    image_path = os.path.join(output_dir, image_filename)

                    if(isInvoice(image_path)):
                        print("Invoice detected")


                    cv2.imwrite(image_path, cropped_image)
                    print(f"Saved {class_name} as {image_filename} in {output_dir}")
                    image_counter += 1

                    # Set the flag to prevent saving multiple copies
                    image_captured = True

    # Reset the flag if the object is no longer in the frame
    if len(results) == 0 or (all(box.cls[0].item() != class_id for box in boxes) and image_captured):
        image_captured = False

    # Display the resulting frame
    cv2.imshow('YOLO Inovice Detection', frame)

    # Press 'q' to exit the webcam window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
