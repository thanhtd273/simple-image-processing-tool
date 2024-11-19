import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

def open_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    if file_path:
        # Open the image and display it
        img = Image.open(file_path)
        img.thumbnail((400, 400))  # Resize for display
        img_tk = ImageTk.PhotoImage(img)
        
        # Update the label with the image
        image_label.config(image=img_tk)
        image_label.image = img_tk
        file_name = os.path.basename(file_path)
        status_label.config(text=f"Loaded: {file_name}")

# Create the main application window
root = tk.Tk()
root.title("Image Processing Application")
root.geometry("500x500")

# Button to open an image
open_button = tk.Button(root, text="Choose Image", command=open_image)
open_button.pack(pady=20)

# Label to display the selected image
image_label = tk.Label(root)
image_label.pack()

# Label to display status
status_label = tk.Label(root, text="No image loaded.", fg="blue")
status_label.pack(pady=10)

# Run the application
root.mainloop()
