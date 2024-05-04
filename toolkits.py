class LoadImageFromLocalPath:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {},
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

    def load_image(self):
        return (
            100,
            200,
        )
