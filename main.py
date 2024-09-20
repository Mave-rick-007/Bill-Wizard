import tkinter as tk
from tkinter import filedialog, Label
from PIL import Image, ImageTk
import cv2
import os

# Initialize the camera
cap = cv2.VideoCapture(0)

# Function to process image
def process_image(image):
    print("Processing image...")

# Function to capture and save the image
def capture_image():
    global frame
    if frame is not None:
        cv2.imwrite("captured_image.jpg", frame)
        img = Image.open("captured_image.jpg")
        resize_and_display_image(img)
        process_image(frame)

# Function to show live camera feed
def show_frame():
    global frame
    ret, frame = cap.read()
    if ret:
        # Convert frame to RGB (OpenCV uses BGR by default)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        img = ImageTk.PhotoImage(image=img)
        
        # Update the label with the live image
        label_img.config(image=img)
        label_img.image = img
        
    # Call show_frame again after 10 milliseconds
    root.after(10, show_frame)

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

# Set the window to open maximized with window controls (cross-platform)
root.update_idletasks()
root.attributes('-zoomed', True)  # This works on Windows, but not on all Linux systems
root.state('normal')  # Default normal state
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")  # Maximize the window

# Create buttons
btn_capture = tk.Button(root, text="Capture Image", command=capture_image)
btn_capture.pack(pady=10, fill=tk.BOTH, expand=True)

btn_insert = tk.Button(root, text="Insert Image/Video", command=insert_file)
btn_insert.pack(pady=10, fill=tk.BOTH, expand=True)

# Label to show live camera feed or image
label_img = Label(root)
label_img.pack(pady=10, fill=tk.BOTH, expand=True)

# Start showing live camera feed
show_frame()

# Run application
root.mainloop()

# Release the camera when the window is closed
cap.release()