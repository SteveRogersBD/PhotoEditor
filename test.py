import requests
import cv2
import numpy as np
import matplotlib.pyplot as plt


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
    edges = cv2.Canny(gray_image, threshold1=30, threshold2=300)

    return edges  # Return the edges for further processing


# Function to plot edge points
def plot_edge_points(edges):
    # Get the coordinates of edge points
    y_coords, x_coords = np.where(edges > 0)  # Get the y and x coordinates of edge pixels

    # Create a scatter plot of edge points
    plt.figure(figsize=(10, 6))
    plt.scatter(x_coords, y_coords, color='red', s=1)  # Use a small size for better visibility
    plt.title('Edge Points')
    plt.xlabel('X coordinates')
    plt.ylabel('Y coordinates')

    plt.gca().invert_yaxis()  # Invert the y-axis to match the image coordinates
    plt.grid(True)  # Optional: Add grid for better visibility
    plt.show()


# Main function
def main():
    # Replace with your actual image path and API key
    image_path = 'obama.png'  # Update this path to your input image
    api_key = 'H1e1Bp798Sr1ZH3gfSygaTQU'  # Replace with your actual API key

    # Remove background
    output_image_path = remove_bg(image_path, api_key)

    if output_image_path:  # Check if the output image path is valid
        # Detect edges in the processed image
        edges = detect_edges(output_image_path)

        if edges is not None:  # Proceed only if edges are detected
            # Plot the edge points
            plot_edge_points(edges)


if __name__ == "__main__":
    main()
