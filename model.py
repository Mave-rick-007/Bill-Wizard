import cv2
from ultralytics import YOLO

model = YOLO('models/yolo-v10s.pt')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    results = model(frame)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Extract bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            # Extract confidence score and class label
            confidence = box.conf[0].item()
            class_id = box.cls[0].item()

            # Get the class name from the model's class names
            class_name = model.names[int(class_id)]

            if (class_name == "bill" or class_name == "invoice") and confidence > 0.3:
                # Draw green bounding box if it's a "bill"
                box_color = (0, 255, 0)
            elif (class_name == "paper" or class_name == "book") and confidence > 0.5:
                # Draw red bounding box for "paper" or "book" that is not a "bill"
                box_color = (0, 0, 255)
            else:
                continue  # Skip if it's not paper/book or bill

            # Draw the bounding box on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            
            # Display label and confidence on the frame
            label_text = f"{class_name} {confidence:.2f}"
            cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow('YOLO Invoice Detection', frame)

    # Press 'q' to exit the webcam window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
