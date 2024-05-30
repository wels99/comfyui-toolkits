from .randseed import *
from .loadimagefromlocalpath import *
from .fixedn import *
from .resizeimage import *

NODE_CLASS_MAPPINGS = {
    "loadimage //dtools": LoadImageFromLocalPath,
    "randseed //dtools": RandSeed,
    "fixedint //dtools": FixedInt,
    "fixedints //dtools": FixedInts,
    "fixedfloat //dtools": FixedFloat,
    "fixedfloats //dtools": FixedFloats,
    "resizeimage //dtools": ResizeImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "loadimage //dtools": "加载本地图片(dtools)",
    "randseed //dtools": "随机数(dtools)",
    "fixedint //dtools": "整数(dtools)",
    "fixedints //dtools": "整数对(dtools)",
    "fixedfloat //dtools": "浮点数(dtools)",
    "fixedfloats //dtools": "浮点数对(dtools)",
    "resizeimage //dtools": "按边缩放图像(dtools)",
}

WEB_DIRECTORY = "./web"
