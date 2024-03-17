import cv2
import argparse 
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_path', type=str, required=True, help='The input file directory')
parser.add_argument('-o', '--output_path', type=str, required=True, help='The output file directory')
args = parser.parse_args()



def linear_interpolation(image1, image2, weight):
    """
    Perform linear interpolation between two images.
    
    Args:
        image1: First input image (numpy array).
        image2: Second input image (numpy array).
        weight: Weight of the second image (between 0 and 1).
        
    Returns:
        Interpolated image (numpy array).
    """
    return cv2.addWeighted(image1, 1 - weight, image2, weight, 0)

def main():
    


if __name__ == "__main__":
    main()
