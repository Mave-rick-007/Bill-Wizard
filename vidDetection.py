import cv2
import os
from ultralytics import YOLO
from isInvoice import isInvoice
import pandas as pd


def invoiceDetector():
    # Load your custom YOLO model
    model = YOLO('weights/yolo-v10s.pt')

    # Path to the directory containing the videos
    video_dir = 'demoVideos/'
    # video_files = [f for f in os.listdir(video_dir) if f.lower().endswith(('.mp4', '.avi', '.mov'))]
    video_files = ['3.mp4']
    # Create the main output directory if it doesn't exist
    output_dir = 'captured_images'
    os.makedirs(output_dir, exist_ok=True)

    invoice_data = pd.DataFrame()

    # Loop through each video in the directory
    for video_file in video_files:
        video_path = os.path.join(video_dir, video_file)
        
        # Open the video file
        cap = cv2.VideoCapture(video_path)

        # Check if the video is opened successfully
        if not cap.isOpened():
            print(f"Error: Could not open video {video_file}")
            continue

        # Create a sub-directory for the current video to save images
        video_output_dir = os.path.join(output_dir, os.path.splitext(video_file)[0])
        os.makedirs(video_output_dir, exist_ok=True)

        # Dictionary to store the highest resolution for each object (by class name) for this video
        object_resolutions = {}

        print(f"Processing video: {video_file}")

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                print(f"Finished processing video: {video_file}")
                break

            # Perform YOLO object detection
            results = model(frame)

            # Loop through detected objects (results contains boxes, confidences, class IDs, etc.)
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

                    # Check if the detected object is 'paper' or 'book'
                    if (class_name == "paper" or class_name == "book") and confidence > 0.5:
                        # Calculate the bounding box area (width * height)
                        box_width = x2 - x1
                        box_height = y2 - y1
                        box_area = box_width * box_height

                        # Check if this is a new detection or if the resolution is higher than the previous one
                        if (class_name not in object_resolutions) or (box_area > object_resolutions[class_name]):
                            # Update the stored resolution for this object in the current video
                            object_resolutions[class_name] = box_area

                            # Draw green bounding box for the object
                            box_color = (0, 255, 0)  # Green
                            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)

                            # Display label and confidence on the frame
                            label_text = f"{class_name} {confidence:.2f}"
                            cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                            # Capture and save the bounded region
                            cropped_image = frame[y1:y2, x1:x2]  # Crop the region inside the bounding box

                            # Use the class name and video name to save the image, overwrite if a higher resolution is found
                            image_filename = f'{class_name}_{video_file}.png'
                            image_path = os.path.join(video_output_dir, image_filename)


                            cv2.imwrite(image_path, cropped_image)
                            curr_data = isInvoice(image_path)
                            if curr_data is not None:
                                print(f"\n\n\n\n{curr_data}\n\n\n\n")
                                invoice_data = pd.concat([invoice_data, curr_data], ignore_index=True)
                                print(f"{invoice_data}\n\n\n\n")
                                
                            print(invoice_data)
                            print(f"Saved/Overwritten {class_name} image for {video_file} in {video_output_dir}")

            # Press 'q' to exit the current video early
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()

    cv2.destroyAllWindows()

    print(invoice_data)
    return invoice_data

invoiceDetector()