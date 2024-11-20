import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageFilter
import numpy as np
import cv2
import os


# Global variables to store images
original_image = None
edited_image = None
def open_image():
    global original_image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    if file_path:
        # Open the image
        original_image = Image.open(file_path)
        # Display in the original image panel
        display_image(original_image, i_label)

def display_image(image, label):
    """Utility function to display an image in a specified label."""
    img = image.copy()
    img.thumbnail((400, 400))  # Resize for display
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk

def apply_filter():
    global original_image, edited_image
    if original_image:
        # Get the selected filter
        selected_filter = filter_var.get()
        edited_image = original_image.copy()

        # Apply the selected filter
        if selected_filter == "Grayscale":
            edited_image = ImageOps.grayscale(edited_image)
        elif selected_filter == "Sepia":
            sepia_image = ImageEnhance.Color(edited_image).enhance(0.3)
            edited_image = ImageOps.colorize(sepia_image.convert("L"), "#704214", "#C0A080")
        elif selected_filter == "Invert":
            edited_image = ImageOps.invert(edited_image.convert("RGB"))
        elif selected_filter == "Gaussian":
            #edited_image = Image.fromarray(cv2.GaussianBlur(np.array(edited_image), (5, 5), 2))
            edited_image = gaussian_filter(np.array(edited_image), sigma=2, radius=2)
        elif selected_filter == "Median":
            edited_image = Image.fromarray(cv2.medianBlur(np.array(edited_image), 5))
            


def remove_background():
    global original_image, edited_image
    if original_image:
        # Get the selected filter
        selected_threshold = rm_var.get()
        edited_image = original_image.copy()
        # Remove BG
        if selected_threshold == "50":
            edited_image = Image.fromarray(np.where(cv2.GaussianBlur(np.array(edited_image), (5, 5), 2) > 50, 50, cv2.GaussianBlur(np.array(edited_image), (5, 5), 2)))
        elif selected_threshold == "100":
            edited_image = Image.fromarray(np.where(cv2.GaussianBlur(np.array(edited_image), (5, 5), 2) > 100, 100, cv2.GaussianBlur(np.array(edited_image), (5, 5), 2)))
        elif selected_threshold == "150":
            edited_image = Image.fromarray(np.where(cv2.GaussianBlur(np.array(edited_image), (5, 5), 2) > 150, 150, cv2.GaussianBlur(np.array(edited_image), (5, 5), 2)))

# Create the main application window
root = tk.Tk()
root.title("Simple photoshop")
root.geometry("850x500")

# Create a split layout using frames
frame = tk.Frame(root, bg="lightgrey")
frame.pack(fill="both", expand=True)

# Label Name
filter_label = tk.Label(frame, text="Choose an action:", bg="lightgrey", font=Font(family="Times New Roman", size=11,weight="bold", slant="italic", underline=1))
filter_label.place(x=0,y=4)

# Label Filter
filter_label = tk.Label(frame, text="Filter", bg="lightgrey", font=("Times New Roman", 10))
filter_label.place(x=125,y=7)

# Dropdown menu Filters
filter_var = tk.StringVar(value="None")
filter_menu = tk.OptionMenu(frame, filter_var, "Grayscale", "Sepia", "Invert", "Gaussian", "Median")
filter_menu.place(x=160, y=3)

# Label Edge Detection
ed_label = tk.Label(frame, text="Edge Detection", bg="lightgrey", font=("Times New Roman", 10))
ed_label.place(x=260,y=7)

# Dropdown menu Edge Detection
ed_var = tk.StringVar(value="None")
ed_menu = tk.OptionMenu(frame, ed_var, "Sobel", "Prewitt", "Robert", "Canny")
ed_menu.place(x=350, y=3)

# Label Remove Background
rm_label = tk.Label(frame, text="Remove BG", bg="lightgrey", font=("Times New Roman", 10))
rm_label.place(x=450,y=7)

# Dropdown menu Remove Background
rm_var = tk.StringVar(value="Threshold")
rm_menu = tk.OptionMenu(frame, rm_var, "50", "100", "150")
rm_menu.place(x=520, y=3)

# Label Image Compression 
ic_label = tk.Label(frame, text="Compress", bg="lightgrey", font=("Times New Roman", 10))
ic_label.place(x=620,y=7)

# Dropdown menu Image Compression
ic_var = tk.StringVar(value="None")
ic_menu = tk.OptionMenu(frame, ic_var, "hihi")
ic_menu.place(x=680, y=3)

# Button Add Image
add_button = tk.Button(frame, text="Add Image +", bg="grey", font=("Times New Roman", 10), command=open_image)
add_button.place(x=760,y=5)

# Create Work Frame
work_frame = tk.Frame(frame, bd=1, relief="solid", bg="white", width=850, height=430)
work_frame.place(x=0,y=35)

# Create the left panel for the original image
left_panel = tk.Frame(work_frame, bd=1, relief="solid", width=425, height=430)
left_panel.pack(side="left", fill="both", expand=True)

# Create the right panel for the filtered image
right_panel = tk.Frame(work_frame, bd=1, relief="solid", width=425, height=430)
right_panel.pack(side="right", fill="both", expand=True)

# Label Image original
original_label = tk.Label(left_panel, text="Original Image", bg="lightgrey", font=("Times New Roman", 10))
original_label.place(x=170,y=0)

# Label in Image
i_label = tk.Label(left_panel, text="Input show here", font=Font(family="Times New Roman", size=10, slant="italic"))
i_label.place(x=0,y=20)

# Label Image edited 
edited_label = tk.Label(right_panel, text="Edited Image", bg="lightgrey", font=("Times New Roman", 10))
edited_label.place(x=170,y=0)

# Label out Image
o_label = tk.Label(right_panel, text="Output show here", font=Font(family="Times New Roman", size=10, slant="italic"))
o_label.place(x=0,y=20)

# Button Apply
apply_button = tk.Button(frame, text="Apply", bg="grey", font=("Times New Roman", 10))
apply_button.place(x=790,y=470)

# Run the application
root.mainloop()
