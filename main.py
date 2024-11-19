import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageOps
import os

# Global variables to store images
original_image = None
filtered_image = None

def open_image():
    global original_image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    if file_path:
        # Open the image
        original_image = Image.open(file_path)
        
        # Display in the original image panel
        display_image(original_image, original_label)

        # Display only the file name in the status label
        file_name = os.path.basename(file_path)
        status_label.config(text=f"Loaded: {file_name}")

def apply_filter():
    global original_image, filtered_image
    if original_image:
        # Get the selected filter
        selected_filter = filter_var.get()
        filtered_image = original_image.copy()

        # Apply the selected filter
        if selected_filter == "Grayscale":
            filtered_image = ImageOps.grayscale(filtered_image)
        elif selected_filter == "Sepia":
            sepia_image = ImageEnhance.Color(filtered_image).enhance(0.3)
            filtered_image = ImageOps.colorize(sepia_image.convert("L"), "#704214", "#C0A080")
        elif selected_filter == "Invert":
            filtered_image = ImageOps.invert(filtered_image.convert("RGB"))

        # Display in the filtered image panel
        display_image(filtered_image, filtered_label)

def display_image(image, label):
    """Utility function to display an image in a specified label."""
    img = image.copy()
    img.thumbnail((400, 400))  # Resize for display
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk

# Create the main application window
root = tk.Tk()
root.title("Image Processing Application")
root.geometry("850x500")

# Create a split layout using frames
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

# Create the left panel for the original image
left_panel = tk.Frame(frame, width=400, height=500)
left_panel.pack(side="left", fill="both", expand=True)

# Create the right panel for the filtered image
right_panel = tk.Frame(frame, width=400, height=500)
right_panel.pack(side="right", fill="both", expand=True)

# Original image section
original_label = tk.Label(left_panel, text="Original Image", bg="white", font=("Arial", 14))
original_label.pack(pady=10)

# Filtered image section
filtered_label = tk.Label(right_panel, text="Filtered Image", bg="white", font=("Arial", 14))
filtered_label.pack(pady=10)

# Control buttons and dropdown
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

# Button to open an image
open_button = tk.Button(control_frame, text="Choose Image", command=open_image)
open_button.pack(side="left", padx=10)

# Dropdown menu for selecting filters
filter_var = tk.StringVar(value="Select Filter")
filter_menu = tk.OptionMenu(control_frame, filter_var, "Grayscale", "Sepia", "Invert")
filter_menu.pack(side="left", padx=10)

# Button to apply the selected filter
apply_button = tk.Button(control_frame, text="Apply Filter", command=apply_filter)
apply_button.pack(side="left", padx=10)

# Label to display status with the file name
status_label = tk.Label(control_frame, text="No image loaded.", fg="blue")
status_label.pack(side="left", padx=10)

# Run the application
root.mainloop()
