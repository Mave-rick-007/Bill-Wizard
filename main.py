import tkinter as tk
from tkinter import filedialog, Label, Text, Scrollbar, RIGHT, Y
from PIL import Image, ImageTk
import cv2
import os
import csv
import io

# Global variable for camera object
cap = None

# Mock AI function that processes the image and returns CSV data
def read_function(image):
    # This function simulates processing the image and returning CSV data
    # For this demo, we're generating mock data
    data = [
        ["ID", "Name", "Age", "Score"],
        [1, "John Doe", 28, 90],
        [2, "Jane Smith", 32, 85],
        [3, "Alice Johnson", 24, 92]
    ]

    # Save the data to a CSV format in-memory (mocked result)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(data)
    output.seek(0)
    
    return output.getvalue()

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
        
        # Call the read_function function and display the CSV result
        csv_data = read_function(frame)
        display_csv_data(csv_data)
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

# Function to display CSV data in the text area
def display_csv_data(csv_data):
    # Clear previous content
    text_csv.delete('1.0', tk.END)
    # Insert new CSV content
    text_csv.insert(tk.END, csv_data)

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

# Add a scrollable Text widget to display CSV data
frame_csv = tk.Frame(root)
frame_csv.pack(fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(frame_csv)
scrollbar.pack(side=RIGHT, fill=Y)

text_csv = Text(frame_csv, wrap=tk.NONE, yscrollcommand=scrollbar.set)
text_csv.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=text_csv.yview)

# Run application
root.mainloop()
