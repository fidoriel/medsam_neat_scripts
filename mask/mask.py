import cv2
import numpy as np
import os

def create_mask(first_image_path, second_image_path, final_image):
    image1 = cv2.imread(first_image_path)
    
    if image1 is None:
        print("Error: Cannot read the first image.")
        return
    image2 = cv2.imread(second_image_path)
    
    if image2 is None:
        print("Error: Cannot read the second image.")
        return

    mask = np.all(image1 > [230, 230, 230], axis=-1)
    mask_image = np.stack([mask]*3, axis=-1)
    masked_image2 = np.where(mask_image, image1, image2)
    cv2.imwrite(final_image, masked_image2)


if __name__ == "__main__":
    input_dir = "projections"
    enhanced_dir = "projections_enhanced"
    output_dir = "output"
    for file in os.listdir(input_dir):
        print(file)
        first_image_path = os.path.join(input_dir, file)
        second_image_path = os.path.join(enhanced_dir, file)
        final_image = os.path.join(output_dir, file)
        create_mask(first_image_path, second_image_path, final_image)
