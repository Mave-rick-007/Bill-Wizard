import tkinter as tk
from tkinter import filedialog, Label
from PIL import Image, ImageTk
import cv2
import os

# Global variable for camera object
cap = None

# Function to start live camera feed
def take_photo():
    global cap
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open the camera.")
        return

    # Show the live camera feed
    show_frame()

    # Enable the "Capture" button after starting the camera
    btn_capture.config(state=tk.NORMAL)

# Function to show live camera feed
def show_frame():
    global cap
    ret, frame = cap.read()
    if ret:
        # Convert frame to RGB (OpenCV uses BGR by default)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        img = ImageTk.PhotoImage(image=img)

        # Update the label with the live image
        label_img.config(image=img)
        label_img.image = img

    # Call show_frame again after 10 milliseconds to keep the feed running
    if cap is not None and cap.isOpened():
        root.after(10, show_frame)

# Function to capture and save the image, then close the camera
def capture_image():
    global cap
    ret, frame = cap.read()
    if ret:
        # Save the captured image
        cv2.imwrite("captured_image.jpg", frame)
        img = Image.open("captured_image.jpg")
        resize_and_display_image(img)
        print("Photo captured and saved.")
    else:
        print("Error: Unable to capture image.")

    # Release the camera and close the feed
    cap.release()
    cap = None
    btn_capture.config(state=tk.DISABLED)

# Open file dialog to insert image or video
def insert_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image/Video Files", "*.jpg *.jpeg *.png *.mp4")])
    if file_path:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in [".jpg", ".jpeg", ".png"]:
            img = Image.open(file_path)
            resize_and_display_image(img)
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
btn_take_photo = tk.Button(root, text="Take Photo", command=take_photo)
btn_take_photo.pack(pady=10, fill=tk.BOTH, expand=True)

btn_insert = tk.Button(root, text="Insert Image/Video", command=insert_file)
btn_insert.pack(pady=10, fill=tk.BOTH, expand=True)

# "Capture" button is initially disabled until the camera starts
btn_capture = tk.Button(root, text="Capture", command=capture_image, state=tk.DISABLED)
btn_capture.pack(pady=10, fill=tk.BOTH, expand=True)

# Label to show live camera feed or image
label_img = Label(root)
label_img.pack(pady=10, fill=tk.BOTH, expand=True)

# Run application
root.mainloop()
