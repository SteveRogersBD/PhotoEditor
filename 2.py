import requests
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Added for background image handling


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


# Function to detect edges in the image
def detect_edges(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found or unable to read.")
        return None  # Return None if the image cannot be read

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform edge detection
    edges = cv2.Canny(gray_image, threshold1=150, threshold2=150)

    return edges, image  # Return both edges and the original image


# Function to plot curves based on edge points
def plot_curves(edges):
    # Get the coordinates of edge points
    y_coords, x_coords = np.where(edges > 0)  # Get the y and x coordinates of edge pixels

    # Fit a spline to the edge points
    tck, u = splprep([x_coords, y_coords], s=1)  # s controls the smoothness of the spline
    x_new, y_new = splev(np.linspace(0, 1, 1000), tck)  # Generate new x, y points

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.scatter(x_coords, y_coords, color='red', s=1)  # Plot edge points in red
    plt.title('Fitted Curves of Edge Points')
    plt.xlabel('X coordinates')
    plt.ylabel('Y coordinates')
    plt.xlim(0, edges.shape[1])  # Set x-axis limits to match edge width
    plt.ylim(edges.shape[0], 0)  # Set y-axis limits to match edge height and invert
    plt.grid(True)  # Show grid lines
    plt.show()  # Display the plot


# Main function
def main():
    # Create a Tkinter window
    root = tk.Tk()
    root.geometry('500x300')  # Set window size to 500x300
    root.title("Background Removal and Edge Detection")

    # Load the background image
    bg_image = Image.open("bg.jpeg")
    bg_image = bg_image.resize((500, 300), Image.Resampling.LANCZOS) # Resize the image to match window size
    bg_image_tk = ImageTk.PhotoImage(bg_image)

    # Create a label to display the background image
    bg_label = tk.Label(root, image=bg_image_tk)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window with the background image

    def pick_image():
        image_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp")]
        )

        if not image_path:
            messagebox.showinfo("Info", "No image selected.")
            return  # No image selected

        api_key = 'H1e1Bp798Sr1ZH3gfSygaTQU'  # Update with your API key

        # Remove background
        output_image_path = remove_bg(image_path, api_key)

        if output_image_path:
            # Detect edges in the processed image
            edges, original_image = detect_edges(output_image_path)

            if edges is not None:
                # Plot the curves based on edges
                plot_curves(edges)
            else:
                messagebox.showerror("Error", "Edge detection failed.")
        else:
            messagebox.showerror("Error", "Failed to remove background.")

    # Create and place the button at the bottom center
    pick_button = tk.Button(root, text="Pick Image", command=pick_image)
    pick_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)  # Bottom center position

    root.mainloop()  # Run the Tkinter main loop


if __name__ == "__main__":
    main()
