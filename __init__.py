"""
@author: shahkoorosh
@title: ComfyUI-PersianText
@nickname: PersianText
@description: A powerful ComfyUI node for rendering text with advanced styling options, including full support for Persian/Farsi and Arabic scripts.
"""

import importlib
import os
import sys
from pathlib import Path

# ANSI escape codes for colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"

# Global mappings expected by ComfyUI
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Canonical module flag to prevent double-loading
_init_flag = "__PersianText_initialized__"
if _init_flag in sys.modules:
    pass  # Already initialized
else:
    sys.modules[_init_flag] = True

    def print_colored_bordered(text, text_color, border_color):
        """Print a centered header with a colored border."""
        lines = text.split('\n')
        max_line_length = max(len(line) for line in lines)
        border = f"{border_color}{'─' * (max_line_length + 4)}{RESET}"
        print(f"\n{border}", flush=True)
        for line in lines:
            print(f"{border_color}│ {RESET}{text_color}{line.center(max_line_length)}{RESET}{border_color} │{RESET}", flush=True)
        print(f"{border}\n", flush=True)

    def print_message(message, color):
        """Print a message with the specified color."""
        print(f"{color}{message}{RESET}", flush=True)

    # Print banner
    print_colored_bordered("ComfyUI-PersianText Initialization", YELLOW, CYAN)

    # Load node files
    current_dir = Path(__file__).parent
    for filename in os.listdir(current_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"{current_dir.stem}.{filename[:-3]}"
            try:
                node_module = importlib.import_module(module_name)
                if hasattr(node_module, "NODE_CLASS_MAPPINGS"):
                    NODE_CLASS_MAPPINGS.update(node_module.NODE_CLASS_MAPPINGS)
                if hasattr(node_module, "NODE_DISPLAY_NAME_MAPPINGS"):
                    NODE_DISPLAY_NAME_MAPPINGS.update(
                        node_module.NODE_DISPLAY_NAME_MAPPINGS)
            except Exception as e:
                print_message(f"Error loading {module_name}: {e}", RED)

    # Print loaded node display names
    print_message("Loaded custom nodes:", GREEN)
    for display_name in NODE_DISPLAY_NAME_MAPPINGS.values():
        print_message(display_name, CYAN)

    print("\n", flush=True)
