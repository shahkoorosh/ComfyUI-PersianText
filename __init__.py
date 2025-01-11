"""
@author: ShahKoorosh
@title: ComfyUI-KGnodes
@nickname: KGnodes
@description: This Custom node offers various experimental nodes to make it easier to use ComfyUI.
"""

from .PersianText import PersianText

NODE_CLASS_MAPPINGS = {
    "PersianText": PersianText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PersianText": "PersianText",
}