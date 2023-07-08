import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
import scipy

import cv2
import os
import time
from hashlib import md5

IDIR = "C:/Users/PC/Desktop/Scrapper/Collection"
os.chdir(IDIR)
os.getcwd()

imageFiles = os.listdir()
print(len(imageFiles))

def filter_images(images):
    image_list = []
    for image in images:
        try:
            img = Image.open(image)
            img = img.convert("RGB")  # Convert to RGB mode
            mode = img.mode
            if mode == "RGB":
                image_list.append(image)
            else:
                print(f"Ignoring {image} - Not an RGB image")
        except Exception as e:
            print(f"Ignoring {image} - Error: {str(e)}")
    return image_list


def img_gray(image):
    image = Image.open(image).convert('L')
    return np.array(image)



def resize(image, height=30, width=30):
    row_res = cv2.resize(image,(height, width), interpolation = cv2.INTER_AREA).flatten()
    col_res = cv2.resize(image,(height, width), interpolation = cv2.INTER_AREA).flatten('F')
    return row_res, col_res

def intensity_diff(row_res, col_res):
    difference_row = np.diff(row_res)
    difference_col = np.diff(col_res)
    difference_row = difference_row > 0
    difference_col = difference_col > 0
    return np.vstack((difference_row, difference_col)).flatten()

def file_hash(array):
    return md5(array).hexdigest()

def difference_score(image, height=30, width=30):
    gray = img_gray(image)
    row_res, col_res = resize(gray, height, width)
    difference = intensity_diff(row_res, col_res)
    return difference

def difference_score_dict_hash(image_list):
    ds_dict = {}
    duplicates = []
    hash_ds = []
    for image in image_list:
        ds = difference_score(image)
        hash_ds.append(ds)
        filehash = md5(ds).hexdigest()
        if filehash not in ds_dict:
            ds_dict[filehash] = [image]
        else:
            ds_dict[filehash].append(image)
            duplicates.append((image, ds_dict[filehash]))
    
    return duplicates, ds_dict, hash_ds

def hamming_distance(image, image2):
    score = scipy.spatial.distance.hamming(image, image2)
    return score

def difference_score_dict(image_list):
    ds_dict = {}
    duplicates = []
    for image in image_list:
        ds = difference_score(image)
        if image not in ds_dict:
            ds_dict[image] = ds
        else:
            duplicates.append((image, ds_dict[image]))
    
    return duplicates, ds_dict

image_files = filter_images(imageFiles)
duplicates, ds_dict, hash_ds = difference_score_dict_hash(image_files)

print("Duplicates found:")
for duplicate in duplicates:
    image1, image2_list = duplicate
    print(f"Duplicate images: {image1}")
    for image2 in image2_list:
        print(f" - {image2}")

print("Total duplicates found:", len(duplicates))