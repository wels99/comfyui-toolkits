import os, random, time


class LoadImageFromLocalPath:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = (
        # "IMAGE",
        "INT",
        "INT",
    )

    RETURN_NAMES = (
        # "IMAGE",
        "Width",
        "Height",
    )

    CATEGORY = "tools"
    FUNCTION = "load_image"

    def load_image(self, path: str, **kwargs):
        if not os.path.isfile(path):
            raise FileNotFoundError(f'File "{path}" not found.')
        return (
            100,
            200,
        )

    @classmethod
    def IS_CHANGED(self, **kwargs):
        return time.time()
