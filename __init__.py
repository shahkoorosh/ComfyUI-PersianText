"""
@author: ShahKoorosh
@title: ComfyUI-PersianText
@nickname: PersianText
@description: A powerful ComfyUI node for rendering text with advanced styling options, including full support for Persian/Farsi and Arabic scripts.
"""

from .PersianText import PersianText

NODE_CLASS_MAPPINGS = {
    "PersianText": PersianText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PersianText": "PersianText",
}
