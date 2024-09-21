import tkinter as tk
from tkinter import filedialog, Label, Text, Scrollbar, RIGHT, Y
from PIL import Image, ImageTk
import cv2
import os
import csv
import io
import vidDetection

# Global variable for camera object
cap = None

# Variable to track theme (light or dark mode)
is_dark_mode = False

# Function to toggle between light and dark modes
def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    update_theme()

# Function to update theme based on the current mode
def update_theme():
    if is_dark_mode:
        # Dark mode colors
        bg_color = "#333333"
        fg_color = "#FFFFFF"
        btn_color = "#444444"
    else:
        # Light mode colors
        bg_color = "#FFFFFF"
        fg_color = "#000000"
        btn_color = "#DDDDDD"

    # Update window background
    root.config(bg=bg_color)

    # Update button colors
    btn_take_photo.config(bg=btn_color, fg=fg_color)
    btn_insert.config(bg=btn_color, fg=fg_color)
    btn_capture.config(bg=btn_color, fg=fg_color)
    btn_toggle_theme.config(bg=btn_color, fg=fg_color)

    # Update text widget colors
    text_csv.config(bg=bg_color, fg=fg_color)

    # Update label (for image display) background
    label_img.config(bg=bg_color)


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
        # csv_data = read_function(frame)
        # display_csv_data(csv_data)
    else:
        print("Error: Unable to capture image.")

    # Release the camera and close the feed
    cap.release()
    cap = None
    btn_capture.config(state=tk.DISABLED)

# Open file dialog to insert image or video
def insert_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image/Video Files", "*.jpg *.jpeg *.png *.mp4 *.avi *.mov")])
    if file_path:
        detected_frame = vidDetection.invoiceDetector(file_path)
        if detected_frame is not None:
            csv_buffer = io.StringIO()
            detected_frame.to_csv(csv_buffer)
            csv_string = csv_buffer.getvalue()
            display_csv_data(csv_string)

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
root.attributes('-fullscreen')  # This works on Windows, but not on all Linux systems
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

# Button to toggle light/dark mode
btn_toggle_theme = tk.Button(root, text="Toggle Theme", command=toggle_theme)
btn_toggle_theme.pack(pady=10, fill=tk.BOTH, expand=True)

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

# Initialize with the default (light) theme
update_theme()

# Run application
root.mainloop()
