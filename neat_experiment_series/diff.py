import os
import argparse
from wand.image import Image
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity
import cv2
import numpy as np
import math

def load_image_and_crop(img_path):
    # crop pepper
    # up_left = (400, 102)
    # size = (660, 560)

    # crop coral
    up_left = (315, 226)
    size = (822, 489)

    img = Image(filename=img_path)
    img.crop(up_left[0], up_left[1], width=size[0], height=size[1])
    img.save(filename="test.png")
    return img

def calc_rmsd(base_image_path, compare_image_path):
    # this calculates the root mean square deviation between two images
    base_img = load_image_and_crop(base_image_path)
    comp_img = Image(filename=compare_image_path)
    base_img.fuzz = 0.25 * base_img.quantum_range
    _, diff_val = base_img.compare(comp_img, 'root_mean_square')
    return diff_val

def calc_ssim(base_image_path, compare_image_path):
    # this calculates the structural similarity index between two images

    # use load_image_and_crop for wand images from bytestream
    base_img = cv2.imdecode(np.frombuffer(load_image_and_crop(base_image_path).make_blob("png"), np.uint8), cv2.IMREAD_COLOR)
    comp_img = cv2.imdecode(np.frombuffer(load_image_and_crop(compare_image_path).make_blob("png"), np.uint8), cv2.IMREAD_COLOR)
    gray_base = cv2.cvtColor(base_img, cv2.COLOR_BGR2GRAY)
    gray_comp = cv2.cvtColor(comp_img, cv2.COLOR_BGR2GRAY)
    (score, diff) = structural_similarity(gray_base, gray_comp, full=True)
    return score

def calc_psnr(base_image_path, compare_image_path):
    # this calculates the peak signal-to-noise ratio between two images
    base_img = cv2.imdecode(np.frombuffer(load_image_and_crop(base_image_path).make_blob("png"), np.uint8), cv2.IMREAD_COLOR)
    comp_img = cv2.imdecode(np.frombuffer(load_image_and_crop(compare_image_path).make_blob("png"), np.uint8), cv2.IMREAD_COLOR)
    mse = np.mean((base_img - comp_img) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr

def analyze_experiment_images(directory_path, base_image_path, algorithm='ssim'):
    diff_results = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".png"):
            experiment_value = int(os.path.splitext(filename)[0])
            compare_image_path = os.path.join(directory_path, filename)
            if algorithm == 'ssim':
                diff_val = calc_ssim(base_image_path, compare_image_path)
            elif algorithm == 'rmsd':
                diff_val = calc_rmsd(base_image_path, compare_image_path)
            elif algorithm == 'psnr':
                diff_val = calc_psnr(base_image_path, compare_image_path)
            else:
                raise ValueError('Invalid algorithm specified. Must be ssim, rmsd, or psnr.')
            # normalized_diff = diff_val / experiment_value
            # diff_results[experiment_value] = normalized_diff
            diff_results[experiment_value] = diff_val
    return diff_results

def plot_graph(diff_results, output_path):
    lists = sorted(diff_results.items())
    x, y = zip(*lists)

    plt.plot(x, y, marker='o')
    plt.xticks(x)
    plt.xlabel('Dataset Image Count')
    plt.ylabel('Quality per Image (Diff / Experiment Img Count)')
    plt.title('Quality per Image in Reconstruction Results using Highest Quality Reconstruction as Base')
    plt.grid(True)
    plt.savefig(output_path)
    # plt.show()

parser = argparse.ArgumentParser(description='Process images to calculate and plot differences.')
parser.add_argument('base_image', help='The path to the base image file.')
parser.add_argument('directory', help='The path to the directory containing experiment images.')
parser.add_argument('--algorithm', '-a', help='The algorithm to use for comparison. ssim, psnr or rmsd', default='ssim', choices=['ssim', 'psnr', 'rmsd'])
parser.add_argument('--output', '-o', help='The path to the output file for the graph.', default='output.png')
args = parser.parse_args()

if __name__ == "__main__":
    diff_results = analyze_experiment_images(args.directory, args.base_image, args.algorithm)
    plot_graph(diff_results, args.output)
