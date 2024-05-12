import os, time, random
from PIL import Image, ImageOps, ImageSequence
from PIL.PngImagePlugin import PngInfo
import torch
import numpy as np
import hashlib
import folder_paths
import shutil


class LoadImageFromLocalPath:
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix = f"LIFLP_temp_{time.time()}_" + "".join(
            random.choice("abcdefghijklmnopqrstupvxyz") for x in range(10)
        )
        pass

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "图片路径": (
                    "STRING",
                    {"default": ""},
                ),
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
    FUNCTION = "load_image"

    def load_image(self, **kwargs):
        self.validate_inputs(**kwargs)

        imgpath = self.strip(kwargs["图片路径"])
        ext = imgpath.split(".")[-1]
        tmpfile = self.prefix + "." + ext
        tmpfilepath = os.path.join(self.output_dir, tmpfile)
        shutil.copyfile(imgpath, tmpfilepath)

        img = Image.open(imgpath)
        output_images = []
        output_masks = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            if i.mode == "I":
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if "A" in i.getbands():
                mask = np.array(i.getchannel("A")).astype(np.float32) / 255.0
                mask = 1.0 - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]
        return {
            "ui": {
                "images": (
                    {
                        "filename": tmpfile,
                        "subfolder": "",
                        "type": self.type,
                    },
                )
            },
            "result": (
                output_image,
                output_mask,
                img.width,
                img.height,
            ),
        }

    @classmethod
    def IS_CHANGED(self, **kwargs):
        self.validate_inputs(**kwargs)

        imgpath = self.strip(kwargs["图片路径"])
        m = hashlib.sha256()
        with open(imgpath, "rb") as f:
            m.update(f.read())
        return m.digest().hex()

    def validate_inputs(self, **kwargs):
        image_path = self.strip(kwargs["图片路径"])
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f'File "{image_path}" not found.')
        return True

    def strip(self, ipath: str) -> str:
        return ipath.strip('"').strip("'")
