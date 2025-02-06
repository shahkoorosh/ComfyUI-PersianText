import os
import torch
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageFilter
from arabic_reshaper import reshape
import numpy as np
from .utils.colors import COLORS, color_mapping

class PersianText:

    def __init__(self):

        pass

    @classmethod
    def INPUT_TYPES(s):

        fonts_dir = os.path.join(os.path.dirname(__file__), "Fonts")
        available_fonts = [f for f in os.listdir(fonts_dir) if f.endswith('.ttf')]
        default_font = available_fonts[0] if available_fonts else "BYekan.ttf" if "BYekan.ttf" in available_fonts else available_fonts[0] if available_fonts else None

        if not default_font:
            print(f"Warning: No fonts found in {fonts_dir}. Using default PIL font.")

        font_options = available_fonts if available_fonts else [default_font] if default_font else []

        return {
            "required": {
                "Image Width": ("INT", {"default": 512, "min": 1, "max": 4096, "step": 1}),
                "Image Height": ("INT", {"default": 512, "min": 1, "max": 4096, "step": 1}),
                "Text": ("STRING", {"multiline": True, "dynamicPrompts": True, "default": "سلام کامفی"}),
                "Font": (font_options, {"default": default_font}) if font_options else (["default_font"], {"default": "default_font"}), # Handle case with no fonts
                "Size": ("INT", {"default": 60, "min": 1, "max": 9999, "step": 1}),
                "Text Color": (COLORS, {"default": "black"}),
                "Background Color": (COLORS, {"default": "white"}),
                "Horizontal Align": (["left", "center", "right"], {"default": "center"}),
                "Vertical Align": (["top", "center", "bottom"], {"default": "center"}),
                "Rotation": ("FLOAT", {"default": 0.0, "min": -360, "max": 360, "step": 0.1}),
                "Offset X": ("INT", {"default": 0, "min": -4096, "max": 4096, "step": 1}),
                "Offset Y": ("INT", {"default": 0, "min": -4096, "max": 4096, "step": 1}),
                "Shadow Distance": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1}),
                "Shadow Blur": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1}),
                "Shadow Color": (COLORS, {"default": "black"}),
                "Direction": (["LTR", "RTL"], {"default": "RTL"}),
            },
            "optional": {
                "Text Color Hex": ("STRING", {"multiline": False, "default": "#000000"}),
                "Background Color Hex": ("STRING", {"multiline": False, "default": "#FFFFFF"}),
                "Shadow Color Hex": ("STRING", {"multiline": False, "default": "#000000"}),                
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    FUNCTION = "execute"
    CATEGORY = "🎨KG"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (False, False)


    def process_text(self, text: str, direction: str) -> str:

        lines = text.split('\n')
        processed_lines = []
        for line in lines:
            if direction == "RTL":
                reshaped = reshape(line)
                bidi_text = reshaped[::-1]
            else:
                bidi_text = line
            processed_lines.append(bidi_text)
        return '\n'.join(processed_lines)

    def get_color_values(self, color_name: str, hex_color: str) -> tuple[int, int, int]:

        if color_name == "custom" and hex_color and hex_color.startswith("#"): # Added check for non-empty hex_color
            try:
                return ImageColor.getrgb(hex_color)
            except ValueError:
                print(f"Warning: Invalid hex color code: {hex_color}. Using default color.")
                pass # Fallback to color_mapping or default
        return color_mapping.get(color_name, (0, 0, 0))

    def execute(self, **kwargs):

        text = kwargs.get("Text", "سلام کامفی")
        font = kwargs.get("Font", "BYekan.ttf")
        size = kwargs.get("Size", 60)
        text_color = kwargs.get("Text Color", "black")
        background_color = kwargs.get("Background Color", "white")
        horizontal_align = kwargs.get("Horizontal Align", "center")
        vertical_align = kwargs.get("Vertical Align", "center")
        image_width = kwargs.get("Image Width", 512)
        image_height = kwargs.get("Image Height", 512)
        rotation = kwargs.get("Rotation", 0.0)
        offset_x = kwargs.get("Offset X", 0)
        offset_y = kwargs.get("Offset Y", 0)
        shadow_distance = kwargs.get("Shadow Distance", 0)
        shadow_blur = kwargs.get("Shadow Blur", 0)
        shadow_color = kwargs.get("Shadow Color", "black")
        direction = kwargs.get("Direction", "RTL")
        text_color_hex = kwargs.get("Text Color Hex", "#000000")
        background_color_hex = kwargs.get("Background Color Hex", "#FFFFFF")
        shadow_color_hex = kwargs.get("Shadow Color Hex", "#000000")
        padding = kwargs.get("Padding", 0)

        # Process text for RTL if needed
        bidi_text = self.process_text(text, direction)

        # Load font, use default PIL font if specified font not found or in case of error
        fonts_dir = os.path.join(os.path.dirname(__file__), "Fonts")
        font_path = os.path.join(fonts_dir, font)

        try:
            if font == "default_font" or not os.path.exists(font_path): # Handle "default_font" and missing font file
                selected_font = ImageFont.load_default()
                if font != "default_font":
                    print(f"Warning: Font '{font}' not found or 'default_font' selected. Using default PIL font.")
            else:
                selected_font = ImageFont.truetype(font_path, size)
        except IOError:
            selected_font = ImageFont.load_default()
            print(f"Error loading font '{font}'. Using default PIL font.")


        # Create padded canvas
        padded_width = image_width + 2 * padding
        padded_height = image_height + 2 * padding

        # Create layers with RGBA for shadow and text, L for mask
        text_layer = Image.new('RGBA', (padded_width, padded_height), (0, 0, 0, 0))
        shadow_layer = Image.new('RGBA', (padded_width, padded_height), (0, 0, 0, 0))
        mask_layer = Image.new('L', (padded_width, padded_height), 0) # Mask is grayscale
        draw = ImageDraw.Draw(text_layer)
        shadow_draw = ImageDraw.Draw(shadow_layer)
        mask_draw = ImageDraw.Draw(mask_layer)

        # Get colors, handle potential invalid hex codes in get_color_values
        text_rgb = self.get_color_values(text_color, text_color_hex)
        background_rgb = self.get_color_values(background_color, background_color_hex)
        shadow_rgb = self.get_color_values(shadow_color, shadow_color_hex)

        # Calculate total text height for vertical alignment
        lines = bidi_text.split('\n')
        total_height = 0
        line_heights = []
        line_spacing = int(selected_font.size * 1.2) # Store line spacing factor
        for i, line in enumerate(lines): # Enumerate to track line index
            if line.strip():
                bbox = selected_font.getbbox(line)
                line_h = bbox[3]
            else:
                line_h = int(selected_font.size * 0.8)
            line_heights.append(line_h)
            total_height += line_h
            if i < len(lines) - 1: # Add line spacing for all lines except the last one
                total_height += line_spacing - line_h # Add the *extra* spacing on top of line height


        # Calculate starting Y position based on vertical alignment
        y = {
            "top": padding + offset_y,
            "center": (padded_height - total_height) // 2 + offset_y,
            "bottom": padded_height - total_height - padding + offset_y
        }[vertical_align]

        # Draw text line by line
        for i, line in enumerate(lines):
            if not line.strip(): # Handle empty lines
                y += int(selected_font.size * 0.8) # Move y down for empty lines, reduced slightly
                continue

            bbox = selected_font.getbbox(line)
            line_width = bbox[2]
            line_height = bbox[3]

            # Calculate X position based on horizontal alignment
            if horizontal_align == "left":
                x = padding + offset_x
            elif horizontal_align == "center":
                x = (padded_width - line_width) // 2 + offset_x
            else:  # "right"
                x = padded_width - line_width - padding + offset_x

            # Draw shadow if shadow_distance > 0
            if shadow_distance > 0:
                shadow_draw.text(
                    (x + shadow_distance, y + shadow_distance),
                    line,
                    font=selected_font,
                    fill=shadow_rgb
                )

            # Draw main text
            draw.text(
                (x, y),
                line,
                font=selected_font,
                fill=text_rgb
            )

            # Draw to mask (white text on black background for mask)
            mask_draw.text(
                (x, y),
                line,
                font=selected_font,
                fill=255 # White for mask
            )

            # Increment y for next line - using a factor of font size for line spacing
            y += int(selected_font.size * 1.2) # Increased line spacing by 20% of font size

        # Apply Gaussian blur to shadow if shadow_blur > 0 and shadow_distance > 0
        if shadow_blur > 0 and shadow_distance > 0:
            shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(shadow_blur))

        # Rotate layers *before* compositing
        if rotation != 0:
            rotated_text_layer = text_layer.rotate(rotation, expand=True, center=(padded_width//2, padded_height//2))
            rotated_shadow_layer = shadow_layer.rotate(rotation, expand=True, center=(padded_width//2, padded_height//2))
            rotated_mask_layer = mask_layer.rotate(rotation, expand=True, center=(padded_width//2, padded_height//2))
        else:
            rotated_text_layer = text_layer
            rotated_shadow_layer = shadow_layer
            rotated_mask_layer = mask_layer

        # Composite layers: background -> shadow -> text
        background = Image.new('RGB', (padded_width, padded_height), background_rgb) # Background is RGB
        background.paste(rotated_shadow_layer, (0, 0), rotated_shadow_layer) # Paste rotated shadow
        background.paste(rotated_text_layer, (0, 0), rotated_text_layer)   # Paste rotated text
        mask_layer = rotated_mask_layer # Use the rotated mask

        # Crop to original image dimensions (no need to resize after rotation anymore as rotation is on layers)
        background = background.crop((padding, padding, padding + image_width, padding + image_height))
        mask_layer = mask_layer.crop((padding, padding, padding + image_width, padding + image_height))


        # Convert PIL images to torch tensors, normalize image to 0-1, mask to 0-1
        image_np = np.array(background).astype(np.float32) / 255.0
        mask_np = np.array(mask_layer).astype(np.float32) / 255.0

        # Return image and mask tensors as a tuple
        return (torch.from_numpy(image_np).unsqueeze(0), torch.from_numpy(mask_np).unsqueeze(0))


NODE_CLASS_MAPPINGS = {
    "PersianText": PersianText
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PersianText": "Persian Text Generator"
}
