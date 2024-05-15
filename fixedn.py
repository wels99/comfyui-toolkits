import os, random, time

NUM_REPEAT = 4


class Fixedn:
    CATEGORY = "tools"
    FUNCTION = "out"

    def out(self, **kwargs):
        return list(x for x in kwargs.values())


class FixedInt(Fixedn):
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "整数": (
                    "INT",
                    {"default": 1024, "min": 0, "max": 0xFFFFFFFFFFFFFFFF},
                ),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("整数",)


class FixedInts(Fixedn):
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                f"整数{x:02}": (
                    "INT",
                    {"default": 1024, "min": 0, "max": 0xFFFFFFFFFFFFFFFF},
                )
                for x in range(NUM_REPEAT)
            },
        }

    RETURN_TYPES = list("INT" for x in range(NUM_REPEAT))
    RETURN_NAMES = list(f"整数{x:02}" for x in range(NUM_REPEAT))


class FixedFloat(Fixedn):
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "浮点数": ("FLOAT", {"default": 1.0}),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("浮点数",)


class FixedFloats(Fixedn):
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                f"浮点数{x:02}": (
                    "FLOAT",
                    {"default": 1.0},
                )
                for x in range(NUM_REPEAT)
            },
        }

    RETURN_TYPES = list("FLOAT" for x in range(NUM_REPEAT))
    RETURN_NAMES = list(f"浮点数{x:02}" for x in range(NUM_REPEAT))
