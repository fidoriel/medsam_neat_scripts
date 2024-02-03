import os
import shutil
from pathlib import Path
import configparser

DATASET_OUTPUT_DIRECTORY = Path("/host_mount/new_datasets")
ORIGINAL_DATASET_DIRECTORY = Path("/host_mount/dataset")
NEAT_OUTPUT = Path("/host_mount/neat_results")

# input files absolut for neat docker container
TOTAL_IMAGES = 360
ORIGINAL_IMAGE_FOLDER = ORIGINAL_DATASET_DIRECTORY/Path("Pepper")
ORIGINAL_PROJECTIONS_FOLDER = ORIGINAL_IMAGE_FOLDER/Path("projections")
ORIGINAL_TEMP_FOLDER = ORIGINAL_DATASET_DIRECTORY/Path( "pepper")
BASE_INI = ORIGINAL_DATASET_DIRECTORY/ Path("pepper.ini")

# executables
NIKON_TO_NEAT =  Path("/root/neat/build/bin/nikon2neat")
RECONSTRUCT =  Path("/root/neat/build/bin/reconstruct")

# relativ config paths
RELATIVE_TEMP_FOLDER = Path("pepper/")
RELATIVE_TRAIN = RELATIVE_TEMP_FOLDER/ Path("exp_uniform_25/")
TRAIN =  Path("train.txt")
EVAL = Path("eval.txt")
PROJECTIONS = Path("Pepper/projections")
SCENES = Path("/root/neat/scenes")
RELATIVE_CT_CONFIG = Path("Pepper")

def create_xtekct_config(folder: Path, img_count: int) -> None:
    ending = "_CT_parameters.xtekct"
    ini_file = [f for f in os.listdir(ORIGINAL_IMAGE_FOLDER) if f.endswith(ending)][0]
    ini_file = ORIGINAL_IMAGE_FOLDER / ini_file
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(ini_file)

    config["XTekCT"]["Projections"] = str(img_count)
    config["XTekCT"]["AngularStep"] = str(360 / img_count)

    # save the new ini file in the folder
    with open(folder /RELATIVE_CT_CONFIG / f"Pepper{ending}", "w") as configfile:
        config.write(configfile)

def create_ini_config(folder: Path, img_count: int) -> None:
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(BASE_INI)

    with open(folder / f"config.ini", "w") as configfile:
        config.write(configfile)

def create_dataset(folder: Path, img_count: int) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    projections = folder / PROJECTIONS
    projections.mkdir(parents=True, exist_ok=True)

    image_files = sorted([f for f in os.listdir(ORIGINAL_PROJECTIONS_FOLDER) if f.endswith('.tif')])

    # take every n image
    every_n = int(len(image_files) / img_count)
    print(f"every_n: {every_n}th out of {len(image_files)} images for {img_count} images")
    tmp = []
    for i in range(0, len(image_files), every_n):
        tmp.append(image_files[i])
    image_files = tmp

    # copy images
    for image_file in image_files:
        shutil.copy(ORIGINAL_PROJECTIONS_FOLDER / image_file, projections / image_file)

    # create relative temp
    relatiuve_temp = folder / RELATIVE_TRAIN
    relatiuve_temp.mkdir(parents=True, exist_ok=True)

    # eval and train are text files with the image number in each line. they should not overlap. please choose 10% of the images for eval and 10% for train. they shal not overlap
    # create train.txt
    eval_num = 0
    range_to = int(len(image_files) / 10) or 1
    with open(folder/RELATIVE_TRAIN/ TRAIN, "w") as f:
        for i in range(0, len(image_files), range_to):
            f.write(f"{i}\n")
            eval_num += 1

    # create eval.txt
    eval_num = 0
    with open(folder/RELATIVE_TRAIN / EVAL, "w") as f:
        for i in range(int(int(len(image_files))/20), len(image_files), range_to):
            f.write(f"{i}\n")
            eval_num += 1

    # create config
    create_xtekct_config(folder, img_count)
    create_ini_config(folder, img_count)


if __name__ == "__main__":
    DATASET_OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    datasets = []
    experiments = Path("/root/neat/Experiments")

    # clean the experiments directory
    print("Cleaning output folder started")
    r = os.system("rm -rf " + str(experiments) + "/*")
    if r != 0:
        print(f"Cleanup failed")
        exit(1)
    print("Cleaning output folder finished")

    for i in [4, 8, 12, 18, 36, 60, 120, 180, 360]:
        input_folder = DATASET_OUTPUT_DIRECTORY / f"pepper_split_{i}"
        print(f"create dataset with {i} of the images {input_folder}")
        create_dataset(input_folder, i)
        datasets.append(input_folder)

    for dataset in datasets:
        # remove the content of SCENES recursive (keep the folder)
        print("#" * 80)
        print(f"run nikon2neat and reconstruct for {dataset}")
        print("#" * 80)

        # copy the dataset to SCENES rm before
        shutil.copytree(dataset, SCENES, dirs_exist_ok=True)

        # run nikon2neat
        r = os.system(f"{NIKON_TO_NEAT}")
        if r != 0:
            print(f"NIKON_TO_NEAT failed for {dataset}")
            exit(1)

        # run reconstruct
        r = os.system(f"{RECONSTRUCT} scenes/config.ini")
        if r != 0:
            print(f"RECONSTRUCT failed for {dataset}")
            exit(1)

        # rename the first folder starting with 20* to the dataset name, the last folder from dataset
        # get the folderfatching 20* in Experiments

        # get the folderfatching 20* in Experiments
        experiment_folders = [f for f in os.listdir(experiments) if f.startswith("20")]
        folder = experiments / experiment_folders[0]
        # rename the folder
        print(f"rename {folder} to {dataset}")
        final_name = os.path.basename(os.path.normpath(str(dataset)))
        folder.rename(experiments / final_name)

        shutil.copytree(experiments/final_name, NEAT_OUTPUT/final_name, dirs_exist_ok=True)
