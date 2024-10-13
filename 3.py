import requests
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, Label, Button


def remove_bg(image_path, api_key):
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(image_path, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': api_key},
    )
    if response.status_code == requests.codes.ok:
        output_path = 'no-bg.png'
        with open(output_path, 'wb') as out:
            out.write(response.content)
        return output_path  # Return the path of the output image
    else:
        print("Error:", response.status_code, response.text)
        return None  # Return None if there's an error


def detect_edges(image_path, max_size=(200, 200)):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found or unable to read.")
        return None  # Return None if the image cannot be read

    # Resize the image to a maximum of 200x200 pixels
    height, width = image.shape[:2]
    if height > max_size[0] or width > max_size[1]:
        scaling_factor = min(max_size[0] / height, max_size[1] / width)
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
        print(f"Resized image to: {new_size}")  # Print resized dimensions

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, threshold1=50, threshold2=150)

    return edges, image  # Return both edges and the resized original image


def output_curves_as_stars(edges):
    height, width = edges.shape
    for y in range(height):
        line = ''
        for x in range(width):
            if edges[y, x] > 0:  # Edge point
                line += '*'
            else:  # Non-edge point
                line += ' '
        print(line)  # Print each line of the image


class App:
    def __init__(self, master):
        self.master = master
        master.title("Background Removal and Edge Detection")

        self.label = Label(master, text="Select an Image to Remove Background")
        self.label.pack(pady=10)

        self.pick_button = Button(master, text="Pick Image", command=self.pick_image)
        self.pick_button.pack(pady=5)

        self.result_label = Label(master, text="")
        self.result_label.pack(pady=10)

        self.api_key = 'H1e1Bp798Sr1ZH3gfSygaTQU'  # Update with your API key

    def pick_image(self):
        image_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )

        if not image_path:
            return  # No image selected

        self.result_label.config(text="Removing background...")
        output_image_path = remove_bg(image_path, self.api_key)

        if output_image_path:
            self.result_label.config(text="Background removed. Detecting edges...")
            edges, original_image = detect_edges(output_image_path)

            if edges is not None:  # Ensure edges are detected
                output_curves_as_stars(edges)
                self.result_label.config(text="Edge detection complete. Check console for output.")
            else:
                self.result_label.config(text="Edge detection failed.")
        else:
            self.result_label.config(text="Failed to remove background.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
