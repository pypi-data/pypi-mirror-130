# BSDS500 Dataset Loader
"""
    All handlers for BSDS500 dataset. It is recommended to use 
    functions
    - `load_data`: Load the data as dictionary
    - `load_imgs`: Load images only (from data, or freshly)

    Module `BSDS500` has typing classes (for IDE, intellisense, etc.).
    The class is imported as `BSDS500_DataSet`

    Creator: TheProjectsGuy
"""

# Main dataset and class
from . import BSDS500
from .BSDS500 import BSDS500_DataSet

# Functions that help loading data
from .def_load_dataset import load_bsds500_dataset as load_data
from .def_load_dataset import load_imgs_dataset as load_imgs
