from .randseed import *
from .loadimagefromlocalpath import *
from .fixedn import *
from .resizeimage import *

NODE_CLASS_MAPPINGS = {
    "loadimage": LoadImageFromLocalPath,
    "randseed": RandSeed,
    "fixedint": FixedInt,
    "fixedints": FixedInts,
    "fixedfloat": FixedFloat,
    "fixedfloats": FixedFloats,
    "resizeimage": ResizeImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "loadimage": "加载本地图片",
    "randseed": "随机数",
    "fixedint": "整数",
    "fixedints": "整数对",
    "fixedfloat": "浮点数",
    "fixedfloats": "浮点数对",
    "resizeimage": "按边缩放图像",
}

WEB_DIRECTORY = "./web"
