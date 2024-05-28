import os, random, time


class RandSeed:
    MAX = 0x1F_FFFF_FFFF_FFFF

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "种子": (
                    "INT",
                    {"default": 0, "min": 0, "max": self.MAX},
                ),
                "动作": (
                    [
                        "固定",
                        "增加",
                        "减小",
                        "随机",
                    ],
                    {"default": "随机"},
                ),
                "上次值": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("种子",)
    CATEGORY = "tools"
    FUNCTION = "rand"
    OUTPUT_NODE = True

    def rand(self, **kwargs):
        value = kwargs["种子"]
        act = kwargs["动作"]
        last_value = str(value)

        if act == "固定":
            nvalue = value
        elif act == "增加":
            nvalue = value + 1
        elif act == "减小":
            nvalue = value - 1
        elif act == "随机":
            nvalue = random.randint(0, self.MAX)

        nvalue = max(0, min(nvalue, self.MAX))

        return {
            "ui": {
                "种子": (nvalue,),
                "上次值": (last_value,),
            },
            "result": (value,),
        }

    @classmethod
    def IS_CHANGED(self, **kwargs):
        return time.time()
