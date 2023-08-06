# Main datalines package
"""
    Imports the dataloaders module

    Creator: TheProjectsGuy
"""

# Version
__version_info__ = (0, 1, 0)    # MAJOR.MINOR.PATCH
__version__ = ".".join(map(str, __version_info__))

# Data Loaders
from . import dataloaders
