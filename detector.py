
import numpy as np
import cv2
import os
from PIL import Image
from skimage.metrics import structural_similarity as ssim

def filter_images(images):
    image_list = []
    for image in images:
        try:
            img = Image.open(image)
            mode = img.mode
            if mode == 'RGB':
                image_list.append(image)
            else:
                print(f"Ignoring {image} - Not an RGB image")
        except Exception as e:
            print(f"Ignoring {image} - Error: {str(e)}")
    return image_list

def img_gray(image):
    image = Image.open(image)
    return np.array(image.convert('L'))

def calculate_ssim(image1, image2):
    return ssim(image1, image2)

def find_duplicates_and_similar_images(image_list, threshold):
    duplicates = []
    similar_images = []
    hash_dict = {}

    for image_path in image_list:
        image = img_gray(image_path)
        image_hash = hash(image.data.tobytes())

        if image_hash not in hash_dict:
            hash_dict[image_hash] = image_path
        else:
            duplicates.append((image_path, hash_dict[image_hash]))

        for existing_image in similar_images:
            existing_image_path, _ = existing_image
            existing_image_data = img_gray(existing_image_path)
            similarity_score = calculate_ssim(image, existing_image_data)
            if similarity_score >= threshold:
                similar_images.append((image_path, existing_image_path))

    return duplicates, similar_images

# Example usage
IDIR = "C:/Users/PC/Desktop/Scrapper/Collection"
image_files = filter_images(os.listdir(IDIR))

threshold = 0.9  # Adjust the similarity threshold as per your requirement
duplicates, similar_images = find_duplicates_and_similar_images(image_files, threshold)

# Print duplicates
print("Duplicates:")
for image_pair in duplicates:
    image1, image2 = image_pair
    print(f"{image1} is a duplicate of {image2}")

# Print similar images
print("Similar Images:")
for image_pair in similar_images:
    image1, image2 = image_pair
    print(f"{image1} is similar to {image2}")
