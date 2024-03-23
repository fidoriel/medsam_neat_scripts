import cv2
import pathlib

def linear_interpolation(image1, image2, weight):
    return cv2.addWeighted(image1, 1-weight, image2, weight, 0)

def main():
    input_path = pathlib.Path("./enhanced/projections")
    input_path2 = pathlib.Path("./enhanced/projections_enhanced")
    output_path = pathlib.Path("./enhanced/inter")

    for file in input_path.iterdir():
        if file.is_file():
            print(f"Interpolating {file.name}")
            image1 = cv2.imread(str(file))
            image2 = cv2.imread(str(input_path2 / file.name))
            result = linear_interpolation(image1, image2, 0.5)
            cv2.imwrite(str(output_path / file.name), result)

if __name__ == "__main__":
    main()
