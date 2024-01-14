import os
import shutil
from pathlib import Path

DATASET_OUTPUT_DIRECTORY = Path("./new_datasets")
ORIGINAL_DATASET_DIRECTORY = Path("/root/neat/dataset")
NEAT_OUTPUT = Path("/host_mount/neat_results")
import configparser

# input files absolut for neat docker container
TOTAL_IMAGES = 360
ORIGINAL_IMAGE_FOLDER = ORIGINAL_DATASET_DIRECTORY/Path("Pepper")
ORIGINAL_PROJECTIONS_FOLDER = ORIGINAL_IMAGE_FOLDER/Path("projections")
ORIGINAL_TEMP_FOLDER = ORIGINAL_DATASET_DIRECTORY/Path( "pepper")
BASE_INI =  Path("/code/root/neat/config/pepper.ini")

# executables
NIKON_TO_NEAT =  Path("/root/neat/build/bin/nikon2neat")
RECONSTRUCT =  Path("/root/neat/build/bin/reconstruct")

# relativ config paths
RELATIVE_TEMP_FOLDER = Path("pepper/")
RELATIVE_TRAIN = RELATIVE_TEMP_FOLDER/ Path("exp_uniform_25/")
TRAIN = RELATIVE_TRAIN/ Path("train.txt")
EVAL = RELATIVE_TRAIN/Path("eval.txt")
PROJECTIONS = Path("Pepper/projections")
SCENES = Path("/code/root/neat/scenes")

def create_xtekct_config(folder: Path, img_count: int) -> None:
    # load the first ini file which is named *_CT_parameters.xtekct in ORIGINAL_IMAGE_FOLDER
    ending = "_CT_projections.xtekct"
    ini_file = [f for f in os.listdir(ORIGINAL_IMAGE_FOLDER) if f.endswith(ending)][0]
    ini_file = ORIGINAL_IMAGE_FOLDER / ini_file
    config = configparser.ConfigParser()
    config.read(ini_file)

    config["XTecCT"]["Projections"] = str(img_count)
    config["XTecCT"]["AngularStep"] = str(360 / img_count)

    # save the new ini file in the folder
    with open(folder / f"config{ending}", "w") as configfile:
        config.write(configfile)

def create_ini_config(folder: Path, img_count: int) -> None:
    config = configparser.ConfigParser()
    config.read(BASE_INI)

    with open(folder / f"config.ini", "w") as configfile:
        config.write(configfile)

def create_dataset(folder: Path, img_count: int) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    projections = folder / PROJECTIONS
    projections.mkdir(parents=True, exist_ok=True)

    image_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.tif')])

    # take every n image
    every_n = int(len(image_files) / img_count)
    image_files = image_files[::every_n]

    # copy images
    for image_file in image_files:
        shutil.copy(ORIGINAL_PROJECTIONS_FOLDER / image_file, projections / image_file)

    # create relative temp
    relative_temp = folder / RELATIVE_TEMP_FOLDER
    relative_temp.mkdir(parents=True, exist_ok=True)

    # eval and train are text files with the image number in each line. they should not overlap. please choose 10% of the images for eval and 10% for train. they shal not overlap
    # create train.txt
    eval_num = 0
    with open(folder / TRAIN, "w") as f:
        for i in range(0, len(image_files), int(len(image_files) / 10)):
            f.write(f"{i}\n")
            eval_num += 1
    
    # create eval.txt
    eval_num = 0
    with open(folder / EVAL, "w") as f:
        for i in range(int(len(image_files)), len(image_files), int(len(image_files) / 10)):
            f.write(f"{i}\n")
            eval_num += 1
    
    # create config
    create_xtekct_config(folder, img_count)
    create_ini_config(folder, img_count)    


if __name__ == "__name__":
    split_percentages = [1, 0.5, 0.25, 0.125, 0.1, 0.0625]
    datasets = []
    for i in split_percentages:
        input_folder = DATASET_OUTPUT_DIRECTORY / f"pepper_split_{i}"
        create_dataset(input_folder, int(TOTAL_IMAGES * i))
        datasets.append(input_folder) 

    for dataset in datasets:
        # remove the content of SCENES recursive (keep the folder)
        for f in os.listdir(SCENES):
            if os.path.isdir(SCENES / f):
                shutil.rmtree(SCENES / f)
            else:
                os.remove(SCENES / f)
        
        # copy the dataset to SCENES
        shutil.copytree(dataset, SCENES)

        # run nikon2neat
        os.system(f"{NIKON_TO_NEAT}")

        # run reconstruct
        os.system(f"{RECONSTRUCT} scenes/config.ini")


    # copy experiments to final folder
    experiments = Path("/root/neat/Experiments")
    for f in os.listdir(experiments):
        if os.path.isdir(experiments / f):
            shutil.copytree(experiments / f, NEAT_OUTPUT / f)
        else:
            shutil.copy(experiments / f, NEAT_OUTPUT / f)


