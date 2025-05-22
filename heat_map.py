import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog

# Select input directory
def select_directory(title="Select Directory"):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory(title=title)
    return folder_path

# Select input directory
input_dir = select_directory("Select Input Directory (Screenshots)")

if not input_dir:
    print("Input directory not selected properly. Exiting.")
    exit()

# Fixed output directory
output_dir = r"C:\Games\Popitka\EyePy\output"
os.makedirs(output_dir, exist_ok=True)

file_path = os.path.join(input_dir, 'coordinates.txt')
coordinates = []
screenshot_dict = {}

with open(file_path, 'r') as file:
    current_screenshot = None
    for line in file:
        if "Screenshot" in line:
            current_screenshot = line.split("saved at: ")[1].strip()
            screenshot_path = os.path.join(input_dir, os.path.basename(current_screenshot))
            screenshot_dict[screenshot_path] = []
        else:
            try:
                x, y = line.split()
                if current_screenshot:
                    screenshot_dict[screenshot_path].append((float(x), float(y)))
            except ValueError:
                continue

for screenshot_path, coords in screenshot_dict.items():
    if not coords:
        continue

    x_coords, y_coords = zip(*coords)

    # Debugging output
    print(f"Processing {screenshot_path}")
    print(f"X coordinates range from {min(x_coords)} to {max(x_coords)}")
    print(f"Y coordinates range from {min(y_coords)} to {max(y_coords)}")

    # Create a 2D histogram for the heatmap
    x_bins = np.linspace(0, 1920, 96)
    y_bins = np.linspace(0, 1080, 54)

    heatmap, xedges, yedges = np.histogram2d(x_coords, y_coords, bins=[x_bins, y_bins])

    # Apply Gaussian filter
    heatmap = gaussian_filter(heatmap, sigma=3)

    # Create heatmap plot
    plt.figure(figsize=(19.2, 10.8))

    # Load the screenshot as the background image
    try:
        background_img = Image.open(screenshot_path)
        background_img = background_img.resize((1920, 1080))
        plt.imshow(background_img, extent=[0, 1920, 0, 1080], alpha=1.0, aspect='auto')
    except FileNotFoundError:
        print(f"Background image '{screenshot_path}' not found. Proceeding without background.")

    # Overlay heatmap
    plt.imshow(heatmap.T, cmap='hot', origin='lower', extent=[0, 1920, 0, 1080], alpha=0.6)
    plt.colorbar(label='Intensity')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title(f'Heatmap for {os.path.basename(screenshot_path)}')

    # Save heatmap
    output_filename = f'heatmap_{os.path.basename(screenshot_path)}'
    output_path = os.path.join(output_dir, output_filename)
    plt.savefig(output_path)
    plt.close()

print(f"Heatmaps generated and saved to {output_dir}.")
