import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def preprocess_image(image_path):
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        print(f"Error: Unable to read {image_path}.")
        return None
    
    # Normalize the image
    normalized_img = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    
    # Apply Gaussian Blur
    blurred_img = cv2.GaussianBlur(normalized_img, (5, 5), 0)
    
    # Apply CLAHE for contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_img = clahe.apply(blurred_img)
    
    return enhanced_img

def get_image_files(directory):
    # List all files in the directory
    files = os.listdir(directory)
    # Filter out non-image files (assuming all images are .jpg, .jpeg, or .png)
    image_files = [os.path.join(directory, f) for f in files if f.endswith(('.jpg', '.jpeg', '.png'))]
    return image_files

def save_images(images, output_dir):
    # Create the directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i, img in enumerate(images):
        if img is not None:
            # Save the image
            output_path = os.path.join(output_dir, f"processed_image_{i+1}.jpg")
            cv2.imwrite(output_path, img)

# Directories containing the images
bad_images_dir = 'C:/Users/tkate/Desktop/STEMAI/dataset/h1 40x/bad'
good_images_dir = 'C:/Users/tkate/Desktop/STEMAI/dataset/h1 40x/good'

# Output directories for processed images
processed_bad_images_dir = 'C:/Users/tkate/Desktop/STEMAI/dataset/h1 40x/processed_bad'
processed_good_images_dir = 'C:/Users/tkate/Desktop/STEMAI/dataset/h1 40x/processed_good'

# Get list of all image files in the directories
bad_images = get_image_files(bad_images_dir)
good_images = get_image_files(good_images_dir)

# Process bad images
processed_bad_images = [preprocess_image(img) for img in bad_images if preprocess_image(img) is not None]
# Process good images
processed_good_images = [preprocess_image(img) for img in good_images if preprocess_image(img) is not None]

# Save processed images
save_images(processed_bad_images, processed_bad_images_dir)
save_images(processed_good_images, processed_good_images_dir)

# Display the results
def display_images(images, title):
    plt.figure(figsize=(15, 10))
    for i, img in enumerate(images[:6]):  # Display up to 6 images
        plt.subplot(2, 3, i + 1)
        if img is not None:
            plt.imshow(img, cmap='gray')
            plt.title(f"{title} Image {i + 1}")
        else:
            plt.title(f"{title} Image {i + 1} (Not Found)")
        plt.axis('off')
    plt.show()

# Display processed images
display_images(processed_bad_images, "Processed Bad")
display_images(processed_good_images, "Processed Good")
