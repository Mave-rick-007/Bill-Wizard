import tkinter as tk
from tkinter import filedialog, Label
from PIL import Image, ImageTk
import cv2
import os

# Function to process image
def process_image(image):
    print("Processing image...")

# Capture image from camera
def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("captured_image.jpg", frame)
        img = Image.open("captured_image.jpg")
        resize_and_display_image(img)
        process_image(frame)
    cap.release()

# Open file dialog to insert image or video
def insert_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image/Video Files", "*.jpg *.jpeg *.png *.mp4")])
    if file_path:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in [".jpg", ".jpeg", ".png"]:
            img = Image.open(file_path)
            resize_and_display_image(img)
            process_image(img)
        elif ext == ".mp4":
            print("Video file selected")

# Resize image to fit the screen and display
def resize_and_display_image(img):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate maximum size that maintains aspect ratio
    img.thumbnail((screen_width // 2, screen_height // 2))
    img = ImageTk.PhotoImage(img)

    # Display the image
    label_img.config(image=img)
    label_img.image = img

# Create main window
root = tk.Tk()
root.title("Bill-Wizard")

# Make window fullscreen
root.attributes('-fullscreen', True)

# Create buttons
btn_capture = tk.Button(root, text="Capture Image", command=capture_image)
btn_capture.pack(pady=10, fill=tk.BOTH, expand=True)

btn_insert = tk.Button(root, text="Insert Image/Video", command=insert_file)
btn_insert.pack(pady=10, fill=tk.BOTH, expand=True)

# Label to show image
label_img = Label(root)
label_img.pack(pady=10, fill=tk.BOTH, expand=True)

# Exit fullscreen when pressing "Esc"
def exit_fullscreen(event):
    root.attributes('-fullscreen', False)

root.bind("<Escape>", exit_fullscreen)

# Run application
root.mainloop()