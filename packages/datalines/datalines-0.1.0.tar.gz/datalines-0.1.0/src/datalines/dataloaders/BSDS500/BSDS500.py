"""
    The BSDS500 Dataset Module. Contains the BSDS500_DataSet class

    Home page: https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/resources.html

    Creator: TheProjectsGuy
"""

# %% Import modules
import os
import tarfile
import glob
import requests
import copy
from typing import TypedDict
import numpy as np
from PIL import Image
import scipy.io
from tqdm import tqdm


# %% Dataset types
# Ground Truths
class GroundTruthType(TypedDict):
    # Number of annotations (per image)
    na: list[int]
    # Segmentation for every annotator (per image)
    segmentation: list[np.ndarray]
    # Boundaries for every annotator (per image)
    boundaries: list[np.ndarray]

# Full file paths (images and ground truth)
class PathsDict(TypedDict):
    img: list[str]
    gt: list[str]

# Dataset dictionary for training, testing or validation set
class SingleDataSetDict(TypedDict):
    images: list[np.ndarray]
    groundTruth: GroundTruthType
    paths: PathsDict

# Type of the entire dataset (as dictionary)
class DataSetDict(TypedDict):
    training: SingleDataSetDict
    test: SingleDataSetDict
    validation: SingleDataSetDict

# %% Main class
class BSDS500_DataSet:
    """
        Main class for the dataset handling. Initializing object
        ensures that the data is present, call the `load_data`
        function to load (and return) data.

        Constructor Paraemters:
        - zip_file: None or str     default: None
            The location of the 'BSR_bsds500.tgz' ZIP file on system. 
            By default (if None), the zip is stored at location 
            '~/.datalines/datasets/' as 'BSR_bsds500.tgz' on the local
            system. If provided, then this must be an existing file, 
            else the file will be downloaded under the given name.
        - ext_loc: None or str      default: None
            The folder location where files are to be extracted. By
            default (if None), the zip is are extracted at location
            '~/.datalines/datasets/BSDS500/' on local system. If
            provideed, this must be a valid path.
    """
    # Home location (for package)
    __home_loc = "~/.datalines/datasets"
    # ZIP file location (desired) on system
    __dataset_zip_file = f"{__home_loc}/BSR_bsds500.tgz"
    # Destination folder (for extracting)
    __destination_folder = f"{__home_loc}/BSDS500/"
    # URL for dataset
    __download_url = r"http://www.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/BSR/BSR_bsds500.tgz"
    # Data location (in extract, destination folder)
    __data_loc = "BSR/BSDS500/data/" # Data folder
    # Input data in location (relative to __data_loc)
    __x_tr_loc = "images/train/"
    __x_ts_loc = "images/test/"
    __x_vl_loc = "images/val/"
    # Output data in location (relative to __data_loc)
    __y_tr_loc = "groundTruth/train/"
    __y_ts_loc = "groundTruth/test/"
    __y_vl_loc = "groundTruth/val/"
    # Constructor
    def __init__(self, zip_file=None, ext_loc=None) -> None:
        # Configuration
        zf = BSDS500_DataSet.__dataset_zip_file if zip_file is None \
            else zip_file   # Zip file location
        zel = BSDS500_DataSet.__destination_folder if ext_loc is None\
            else ext_loc    # Extraction folder location
        # Properties
        self.zipf_loc = os.path.abspath(os.path.expanduser(zf))
        self.zipext_loc = os.path.abspath(os.path.expanduser(zel))
        self.data_uri = str(BSDS500_DataSet.__download_url)
        # Download dataset
        if self.download_dataset():
            print("Dataset downloaded")
        else:
            print(f"Dataset already present at {self.zipf_loc}")
        # Extract everything
        if self.unzip_tgz():
            print("Files unzipped")
        else:
            print("Folders are already unzipped")
        # Ready to load data (manual call later)
        self.data : DataSetDict = dict()

    # Download the dataset
    def download_dataset(self):
        """
            Downloads the dataset

            Returns:
            - rval: bool
                If the dataset is already downloaded, then 'False' (
                because no download happened). Else if had to download
                then 'True'.
        """
        # Download from URL
        if os.path.exists(self.zipf_loc):
            return False    # Directory already exists
        else:
            url = self.data_uri # URL to use
            resp = requests.get(url, stream=True)   # Request header
            sz = 68    # Size of download (in MB)
            file_name = os.path.basename(self.zipf_loc)
            download_path = os.path.dirname(self.zipf_loc)
            # Create download path (if not existing)
            if not os.path.isdir(download_path):
                os.makedirs(download_path)
            # Download file
            with open(self.zipf_loc, "wb") as fhdlr:
                # Download data in 1 MB chunks
                for data in tqdm(resp.iter_content((1024)**2), 
                    ncols=75, total=sz, desc=file_name, unit="MB"):
                    # Add data to file
                    fhdlr.write(data)
            # Download completed
            return True

    # Unzip files
    def unzip_tgz(self):
        # If path exists, no extraction
        if os.path.exists(self.zipext_loc):
            return False
        else:
            # Extract
            os.makedirs(self.zipext_loc)
            file = tarfile.open(self.zipf_loc)
            file.extractall(self.zipext_loc)   # Extracted
            file.close()
            return True

    # Load the data (images, ground truth)
    def load_data(self) -> DataSetDict:
        """
            Loads all data from the data location and returns the
            dictionary.

            Returns:
            - data: dict
                A dictionary with keys in ["training", "validation",
                "test"]. Each key contains a dict with the keys
                - "images": list of images, each image is of type
                    np.ndarray and shape (H, W, C)
                - "groundTruth": A dictionary having the keys
                    - "na": Number of annotators for the samples (as a
                        list corresponding indices)
                    - "segmentation": list of list of annotated
                        segments for each sample
                    - "boundaries": List of list of annotated
                        boundaries for each sample
                - "paths": A dictionary having the keys
                    - "img": List of strings containing the path to
                        each image sampple. File name with full path,
                        including the '.jpg' extension.
                    - "gt": List of strings containing the path to
                        each '.mat' file containing the segmentation
                        and boundaries (by annotators) for each
                        sample. File name with full path, including
                        the '.mat' extension.
        """
        # Load image, segmentation, boundary sample given the path
        def load_sample(img_path, gt_path):
            """
                Loads a single sample from the corresponding files

                Parameters:
                - img_path: Full path (w .jpg) for image
                - gt_path: Path for ground truth .mat file

                Returns:
                - x_img_np: np.ndarray  shape: (H, W, C)
                    Image having H rows, W columns and C channels
                - y_ann: int
                    Number of annotators for the sample (4 to 9)
                - y_seg: list[np.ndarray]
                    List of (H, W) images containing segments (as int)
                - y_bdr: list[np.ndarray]
                    List of (H, W) images for border (as int - 0, 1)
            """
            # Read image
            x_img_np = np.array(Image.open(img_path)) # (H, W, C)
            # Read .mat file for ground truth
            p_gt = scipy.io.loadmat(gt_path)["groundTruth"]
            y_ann: int = p_gt.shape[1]   # Number of annotators
            # Collect true labels (seg, bdr) from all annotators
            y_seg = [p_gt[0, i]["Segmentation"][0, 0] \
                for i in range(y_ann)]
            y_bdr = [p_gt[0, i]["Boundaries"][0, 0] \
                for i in range(y_ann)]
            return x_img_np, y_ann, y_seg, y_bdr

        # Given paths, retrieve data
        def ret_data(img_path, gt_path):
            """
                Retrieves data samples form paths
                
                Paramters:
                - img_path: str    Images path (*.jpg files)
                - gt_path:  str    Ground truth path (*.mat files)

                Returns:
                - gp_data: SingleDataSetDict    Data retrieved
            """
            # Data
            x_imgs = []     # List of images
            y_anns = []     # Number of annotations
            y_segs = []     # List of list of segmentation annotations
            y_bdrs = []     # List of list of boundary annotations
            # Samples
            img_samples: list[str] = glob.glob(img_path + "/*.jpg")
            gt_samples: list[str] = glob.glob(gt_path + "/*.mat")
            # Assuming files with the same number correspond
            img_samples.sort()
            gt_samples.sort()
            # Load samples into data
            for img_s, gt_s in zip(img_samples, gt_samples):
                x, ya, ys, yb = load_sample(img_s, gt_s)
                # Record all data
                x_imgs.append(x)
                y_anns.append(ya)
                y_segs.append(ys)
                y_bdrs.append(yb)
            gp_data: SingleDataSetDict = {
                # Training images
                "images": copy.deepcopy(x_imgs),
                # Ground truths
                "groundTruth": {
                    "na": copy.deepcopy(y_anns),
                    "segmentation": copy.deepcopy(y_segs),
                    "boundaries": copy.deepcopy(y_bdrs)
                },
                # Corresponding paths
                "paths": {
                    "img": img_samples,
                    "gt": gt_samples
                }
            }
            return gp_data

        # Path to data
        data_path = self.zipext_loc + "/" + \
            BSDS500_DataSet.__data_loc
        # --- Load training data ---
        img_path = os.path.realpath(data_path + \
            BSDS500_DataSet.__x_tr_loc)
        gt_path = os.path.realpath(data_path + \
            BSDS500_DataSet.__y_tr_loc)
        gp_data = ret_data(img_path, gt_path)
        ns = len(gp_data["images"])
        print(f"Loaded {ns} training samples")
        # Save training data
        self.data["training"] = copy.deepcopy(gp_data)
        # --- Load test data ---
        img_path = os.path.realpath(data_path + \
            BSDS500_DataSet.__x_ts_loc)
        gt_path = os.path.realpath(data_path + \
            BSDS500_DataSet.__y_ts_loc)
        gp_data = ret_data(img_path, gt_path)
        ns = len(gp_data["images"])
        print(f"Loaded {ns} test samples")
        # Save test data
        self.data["test"] = copy.deepcopy(gp_data)
        # --- Load validation data ---
        img_path = os.path.realpath(data_path + \
            BSDS500_DataSet.__x_vl_loc)
        gt_path = os.path.realpath(data_path + \
            BSDS500_DataSet.__y_vl_loc)
        gp_data = ret_data(img_path, gt_path)
        ns = len(gp_data["images"])
        print(f"Loaded {ns} validation samples")
        # Save training data
        self.data["validation"] = copy.deepcopy(gp_data)
        return self.data

# %%
if __name__ == "__main__":
    raise ImportError("This script shouldn't run as main")

    # Testing code (for dev)

    # import time
    # start = time.time()
    # ds = BSDS500_DataSet()
    # stop = time.time()
    # print(f"It took {stop - start} to initialize")
    # start = time.time()
    # ds.load_data()
    # stop = time.time()
    # print(f"It took {stop - start} to load")

# %%
