import os
import argparse
from wand.image import Image
import matplotlib.pyplot as plt
from skimage.measure import compare_ssim
import cv2
import numpy as np
import math

def calc_rmsd(base_image_path, compare_image_path):
    # this calculates the root mean square deviation between two images
    with Image(filename=base_image_path) as base_img:
        with Image(filename=compare_image_path) as comp_img:
            base_img.fuzz = 0.25 * base_img.quantum_range
            _, diff_val = base_img.compare(comp_img, 'root_mean_square')
    return diff_val

def calc_ssim(base_image_path, compare_image_path):
    # this calculates the structural similarity index between two images
    base_img = cv2.imread(base_image_path)
    comp_img = cv2.imread(compare_image_path)
    gray_base = cv2.cvtColor(base_img, cv2.COLOR_BGR2GRAY)
    gray_comp = cv2.cvtColor(comp_img, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(gray_base, gray_comp, full=True)
    return score

def calc_psnr(base_image_path, compare_image_path):
    # this calculates the peak signal-to-noise ratio between two images
    base_img = cv2.imread(base_image_path)
    comp_img = cv2.imread(compare_image_path)
    mse = np.mean((base_img - comp_img) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr

def analyze_experiment_images(directory_path, base_image_path):
    diff_results = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".png"):
            experiment_value = int(os.path.splitext(filename)[0])
            compare_image_path = os.path.join(directory_path, filename)
            diff_val = calc_ssim(base_image_path, compare_image_path)
            # normalized_diff = diff_val / experiment_value
            # diff_results[experiment_value] = normalized_diff
            diff_results[experiment_value] = diff_val
    return diff_results

def plot_graph(diff_results):
    lists = sorted(diff_results.items())
    x, y = zip(*lists)

    plt.plot(x, y, marker='o')
    plt.xticks(x)
    plt.xlabel('Dataset Image Count')
    plt.ylabel('Quality per Image (Diff / Experiment Img Count)')
    plt.title('Quality per Image in Reconstruction Results using Highest Quality Reconstruction as Base')
    plt.grid(True)
    plt.show()

parser = argparse.ArgumentParser(description='Process images to calculate and plot differences.')
parser.add_argument('base_image', help='The path to the base image file.')
parser.add_argument('directory', help='The path to the directory containing experiment images.')
args = parser.parse_args()

if __name__ == "__main__":
    diff_results = analyze_experiment_images(args.directory, args.base_image)
    plot_graph(diff_results)
