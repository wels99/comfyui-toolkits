from .randseed import *
from .loadimagefromlocalpath import *

NODE_CLASS_MAPPINGS = {
    "loadimage": LoadImageFromLocalPath,
    "randseed": RandSeed,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "loadimage": "Load Image",
    "randseed": "Random Seed",
}

WEB_DIRECTORY = "./web"
