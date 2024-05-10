import os, random, time


class RandSeed:
    MAX = 0x1F_FFFF_FFFF_FFFF

    def __init__(self):
        self.MAX = 0x1F_FFFF_FFFF_FFFF
        pass

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "value": (
                    "INT",
                    {"default": 0, "min": 0, "max": RandSeed.MAX},
                ),
                "control_after_generate": (
                    [
                        "fixed",
                        "increment",
                        "decrement",
                        "randomize",
                    ],
                    {"default": "randomize"},
                ),
                "last_value": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("Value",)
    CATEGORY = "tools"
    FUNCTION = "rand"
    OUTPUT_NODE = True

    def rand(self, value: int, control_after_generate: str, last_value: str):
        last_value = str(value)

        if control_after_generate == "fixed":
            nvalue = value
        elif control_after_generate == "increment":
            nvalue = value + 1
        elif control_after_generate == "decrement":
            nvalue = value - 1
        elif control_after_generate == "randomize":
            nvalue = random.randint(0, RandSeed.MAX)

        nvalue = max(0, min(nvalue, RandSeed.MAX))

        return {
            "ui": {
                "value": (nvalue,),
                "last_value": (last_value,),
            },
            "result": (value,),
        }

    @classmethod
    def IS_CHANGED(self, **kwargs):
        return time.time()
