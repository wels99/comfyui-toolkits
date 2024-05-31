import os, time, random
from PIL import Image, ImageOps, ImageSequence
from PIL.PngImagePlugin import PngInfo
import torch
import numpy as np
import hashlib
import folder_paths
import shutil
import comfy.utils


class ResizeImage:
    max = 65536
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]
    compress_level = 4

    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.tmpfile = f"Rimg_temp_{time.time()}_" + "".join(
            random.choice("abcdefghijklmnopqrstupvxyz") for x in range(10)
        )
        pass

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "图像": ("IMAGE",),
                "边长": (
                    "INT",
                    {"default": 1024, "min": 10, "max": self.max, "step": 1},
                ),
                "缩放方法": (self.upscale_methods,),
                "缩放基准边": (
                    [
                        "长边",
                        "短边",
                    ],
                    {"default": "长边"},
                ),
            },
            "optional": {
                "遮罩": ("MASK",),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = (
        "IMAGE",
        "MASK",
        "INT",
        "INT",
    )

    RETURN_NAMES = (
        "图像",
        "遮罩",
        "Width",
        "Height",
    )

    CATEGORY = "tools"
    FUNCTION = "resizeimg"

    def resizeimg(self, **kwargs):
        s = kwargs["图像"].movedim(-1, 1)
        l = kwargs["边长"]
        upscale_method = kwargs["缩放方法"]
        scale_base = kwargs["缩放基准边"]
        if "遮罩" in kwargs:
            mask = kwargs["遮罩"]
        else:
            mask = None

        oldwidth = s.shape[3]
        oldheight = s.shape[2]

        if scale_base == "长边":
            scale = l / max(oldwidth, oldheight)
        else:
            scale = l / min(oldwidth, oldheight)

        width = int(oldwidth * scale)
        height = int(oldheight * scale)

        s = comfy.utils.common_upscale(s, width, height, upscale_method, False)
        s = s.movedim(1, -1)

        maskimg = []
        if mask is not None:
            maskimg = (
                mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1]))
                .movedim(1, -1)
                .expand(-1, -1, -1, 3)
            )
            maskimg = maskimg.movedim(-1, 1)
            maskimg = comfy.utils.common_upscale(
                maskimg, width, height, upscale_method, False
            )
            maskimg = maskimg.movedim(1, -1)
            maskimg = maskimg[:, :, :, 0]

        results = list()
        for batch_number, img in enumerate(s):
            tmpfile = f"{self.tmpfile}_{batch_number}.png"
            tmpfilepath = os.path.join(self.output_dir, tmpfile)
            i = 255.0 * img.cpu().numpy()
            i = np.clip(i, 0, 255).astype(np.uint8)
            img = Image.fromarray(i)
            img.save(
                tmpfilepath,
                pnginfo=None,
                compress_level=self.compress_level,
            )
            results.append(
                {
                    "filename": tmpfilepath,
                    "subfolder": "",
                    "type": self.type,
                }
            )

        return {
            "ui": {"images": results},
            "result": (
                s,
                maskimg,
                width,
                height,
            ),
        }
