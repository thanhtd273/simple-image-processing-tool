import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageFilter
import numpy as np
import cv2
from rembg import remove

# Global variables to store images
original_image = None
edited_image = None

# Open image from local
def open_image():
    global original_image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    if file_path:
        # Open the image
        original_image = Image.open(file_path)
        # Display in the original image panel
        display_image(original_image, i_label)

# Display image
def display_image(image, label):
    """Utility function to display an image in a specified label."""
    img = image.copy()
    img.thumbnail((400, 400))  # Resize for display
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk 

def undo_all_change():
    global original_image, edited_image
    if original_image:
        edited_image = original_image.copy()
        display_image(edited_image, o_label)
    else:
        messagebox.showerror("Error", "Please load an image first!")

def gray_filter():
    global original_image, edited_image
    if original_image:
        edited_image = ImageOps.grayscale(original_image)
        display_image(edited_image, o_label)
    else:
        messagebox.showerror("Error", "Please load an image first!")    

def sepia_filter():
    global original_image, edited_image
    if original_image:
        sepia_image = ImageEnhance.Color(original_image).enhance(0.3)
        edited_image = ImageOps.colorize(sepia_image.convert("L"), "#704214", "#C0A080")
        display_image(edited_image, o_label)
    else:
        messagebox.showerror("Error", "Please load an image first!") 

def invert_filter():
    global original_image, edited_image
    if original_image:
        edited_image = ImageOps.invert(original_image.convert("RGB"))
        display_image(edited_image, o_label)
    else:
        messagebox.showerror("Error", "Please load an image first!")    

def gaussian_filter():
    global original_image, edited_image
    if original_image:
        edited_image = Image.fromarray(cv2.GaussianBlur(np.array(original_image), (5, 5), 2))
        display_image(edited_image, o_label)
    else:
        messagebox.showerror("Error", "Please load an image first!")    

def median_filter():
    global original_image, edited_image
    if original_image:
        edited_image = Image.fromarray(cv2.medianBlur(np.array(original_image), 5))
        display_image(edited_image, o_label)
    else:
        messagebox.showerror("Error", "Please load an image first!")

def sobel_edge_detection():
    global original_image, edited_image
    if original_image:
        gray_image = original_image.convert("L")
        img_array = np.array(gray_image)
        sobel_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
        sobel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
        gx = np.zeros_like(img_array, dtype=np.float32)
        gy = np.zeros_like(img_array, dtype=np.float32)
        edited_array = np.zeros_like(img_array, dtype=np.uint8)

        for i in range(1, len(img_array) - 1):
            for j in range(1, len(img_array[0]) - 1):
                gx[i, j] = (sobel_x * img_array[i-1:i+2, j-1:j+2]).sum()
                gy[i, j] = (sobel_y * img_array[i-1:i+2, j-1:j+2]).sum()
                edited_array[i, j] = min(255, np.sqrt(gx[i, j]**2 + gy[i, j]**2))
        edited_image = Image.fromarray(edited_array)
        display_image(edited_image, o_label)
    else:
        messagebox.showerror("Error", "Please load an image first!")

def prewitt_edge_detection():
    global original_image, edited_image
    if original_image:
        gray_image = original_image.convert("L")
        img_array = np.array(gray_image)
        prewitt_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
        prewitt_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        gx = np.zeros_like(img_array, dtype=np.float32)
        gy = np.zeros_like(img_array, dtype=np.float32)
        edited_array = np.zeros_like(img_array, dtype=np.uint8)

        for i in range(1, len(img_array) - 1):
            for j in range(1, len(img_array[0]) - 1):
                gx[i, j] = (prewitt_x * img_array[i-1:i+2, j-1:j+2]).sum()
                gy[i, j] = (prewitt_y * img_array[i-1:i+2, j-1:j+2]).sum()
                edited_array[i, j] = min(255, np.sqrt(gx[i, j]**2 + gy[i, j]**2))
        edited_image = Image.fromarray(edited_array)
        display_image(edited_image, o_label)
    else:
        messagebox.showerror("Error", "Please load an image first!")

def roberts_edge_detection():
    global original_image, edited_image
    if original_image:
        gray_image = original_image.convert("L")
        img_array = np.array(gray_image)
        roberts_x = np.array([[1, 0], [0, -1]])
        roberts_y = np.array([[0, 1], [-1, 0]])
        gx = np.zeros_like(img_array, dtype=np.float32)
        gy = np.zeros_like(img_array, dtype=np.float32)
        edited_array = np.zeros_like(img_array, dtype=np.uint8)

        for i in range(len(img_array) - 1):
            for j in range(len(img_array[0]) - 1):
                gx[i, j] = (roberts_x * img_array[i:i+2, j:j+2]).sum()
                gy[i, j] = (roberts_y * img_array[i:i+2, j:j+2]).sum()
                edited_array[i, j] = min(255, np.sqrt(gx[i, j]**2 + gy[i, j]**2))
        edited_image = Image.fromarray(edited_array)
        display_image(edited_image, o_label)
    else:
        messagebox.showerror("Error", "Please load an image first!")

def canny_edge_detection():
    global original_image, edited_image
    if original_image:
        gray_image = original_image.convert("L")
        img_array = np.array(gray_image)
        smooth_img = cv2.GaussianBlur(img_array, (5, 5), sigmaX=1, sigmaY=1)
        canny_mask = cv2.Canny(smooth_img, 100, 200)
        min_val = np.min(canny_mask)
        max_val = np.max(canny_mask)
        edited_array = (canny_mask - min_val) / (max_val - min_val)
        edited_array *= 255
        edited_image = Image.fromarray(edited_array)
        display_image(edited_image, o_label)
    else:
        messagebox.showerror("Error", "Please load an image first!")

def remove_background():
    global original_image, edited_image
    if original_image:
        edited_image = remove(original_image)
        display_image(edited_image, o_label)
    else:
        messagebox.showerror("Error", "Please load an image first!")

def compress_img():
    global original_image, edited_image
    if original_image:
        quality = tk.simpledialog.askinteger(
            "Compression Quality", 
            "Enter the quality percentage (1-100):", 
            minvalue=1, maxvalue=100
        )
        if quality:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".jpg", 
                filetypes=[("JPEG files", "*.jpg")]
            )
            if file_path:
                original_image.save(file_path, "JPEG", quality=quality)
                edited_image = Image.open(file_path)
                display_image(edited_image, o_label)
                messagebox.showinfo("Success", f"Image compressed and saved to {file_path}")
    else:
        messagebox.showerror("Error", "Please load an image first!")


# Tạo cửa sổ chính
root = tk.Tk()
root.title("Simple Photoshop")
root.geometry("850x500")

# Tạo menu bar
menu_bar = tk.Menu(root)

# Menu File
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Add Image", command=open_image)
file_menu.add_command(label="Undo All Change", command=undo_all_change)
file_menu.add_command(label="Compress Image", command=compress_img)
menu_bar.add_cascade(label="File", menu=file_menu)

# Menu Filter
filter_menu = tk.Menu(menu_bar, tearoff=0)
filter_menu.add_command(label="Grayscale", command=gray_filter)
filter_menu.add_command(label="Sephia", command=sepia_filter)
filter_menu.add_command(label="Invert", command=invert_filter)
filter_menu.add_command(label="Gaussian", command=gaussian_filter)
filter_menu.add_command(label="Median", command=median_filter)
filter_menu.add_separator()
menu_bar.add_cascade(label="Filter", menu=filter_menu)

# Menu Edge Detection
ed_menu = tk.Menu(menu_bar, tearoff=0)
ed_menu.add_command(label="Sobel", command=sobel_edge_detection)
ed_menu.add_command(label="Prewitt", command=prewitt_edge_detection)
ed_menu.add_command(label="Robert", command=roberts_edge_detection)
ed_menu.add_command(label="Canny", command=canny_edge_detection)
menu_bar.add_cascade(label="Edge Detection", menu=ed_menu)

# Menu View
rm_menu = tk.Menu(menu_bar, tearoff=0)
rm_menu.add_command(label="Remove", command=remove_background)
menu_bar.add_cascade(label="Remove background", menu=rm_menu)

root.config(menu=menu_bar)

# Create Work Frame
frame = tk.Frame(root, bg="lightgrey")
frame.pack(fill="both", expand=True)

# Create the left panel for the original image
left_panel = tk.Frame(frame, bd=1, relief="solid", width=425, height=430)
left_panel.pack(side="left", fill="both", expand=True)

# Create the right panel for the filtered image
right_panel = tk.Frame(frame, bd=1, relief="solid", width=425, height=430)
right_panel.pack(side="right", fill="both", expand=True)

# Label Image original
original_label = tk.Label(left_panel, text="Original Image", bg="lightgrey", font=("Times New Roman", 10))
original_label.place(x=170,y=0)

# Label in Image
i_label = tk.Label(left_panel, text="Input show here", font=Font(family="Times New Roman", size=10, slant="italic"), fg="grey")
i_label.place(x=0,y=20)

# Label Image edited 
edited_label = tk.Label(right_panel, text="Edited Image", bg="lightgrey", font=("Times New Roman", 10))
edited_label.place(x=170,y=0)

# Label out Image
o_label = tk.Label(right_panel, text="Output show here", font=Font(family="Times New Roman", size=10, slant="italic"), fg="grey")
o_label.place(x=0,y=20)

# Run
root.mainloop()
