import os
import torch
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageFilter
import arabic_reshaper
import numpy as np
import unicodedata
from bidi.algorithm import get_display
from .utils.colors import COLORS, color_mapping
import re


class PersianText:
    @classmethod
    def INPUT_TYPES(cls):
        font_dir = os.path.join(os.path.dirname(__file__), "Fonts")
        font_files = []
        try:
            font_files = [f for f in os.listdir(font_dir) if f.endswith(('.ttf', '.otf'))]
        except FileNotFoundError:
            font_files = []
        return {
            "required": {
                "Text": ("STRING", {"default": "سلام کامفی", "dynamicPrompts": True, "rows": 5, "multiline": True}),
                "Farsi/Arabic Font": (["default"] + font_files, {"default": "BYekan.ttf"}),
                "English/Latin Font": (["default"] + font_files, {"default": "arial.ttf"}),
                "Size": ("INT", {"default": 60, "min": 1, "max": 256}),
                "Text Color": (COLORS, {"default": "Black"}),
                "Background Color": (COLORS, {"default": "White"}),
                "Horizontal Align": (["left", "center", "right"], {"default": "center"}),
                "Vertical Align": (["top", "center", "bottom"], {"default": "center"}),
                "Image Width": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "Image Height": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "Rotation": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0}),
                "Offset X": ("INT", {"default": 0, "min": -256, "max": 256}),
                "Offset Y": ("INT", {"default": 0, "min": -256, "max": 256}),
                "Shadow Distance": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 256.0}),
                "Shadow Blur": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 256.0}),
                "Shadow Color": (COLORS, {"default": "Black"}),
                "Text Color Hex": ("STRING", {"default": "#000000"}),
                "Background Color Hex": ("STRING", {"default": "#FFFFFF"}),
                "Shadow Color Hex": ("STRING", {"default": "#000000"}),
                "Padding": ("INT", {"default": 0, "min": 0, "max": 256}),
                "Transparent Background": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "execute"
    CATEGORY = "🎨KG"

    def process_text(self, text, direction="auto"):
        def get_script(char):
            category = unicodedata.category(char)
            if char == ' ':
                return "space"
            elif unicodedata.bidirectional(char) in ('AL', 'R', 'AN'):
                return "arabic"
            else:
                return "latin"

        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            if not line.strip():
                processed_lines.append([])
                continue
            
            segments = []
            current_segment = ""
            current_script = None
            
            for char in line:
                script = get_script(char)
                if script == "space" and current_segment:
                    current_segment += char
                elif script != current_script and current_segment:
                    segments.append((current_script, current_segment))
                    current_segment = char
                    current_script = script
                else:
                    current_segment += char
                    current_script = script
            
            if current_segment:
                segments.append((current_script, current_segment))
            
            processed_segments = []
            for script, segment in segments:
                if script == "arabic":
                    reshaped = arabic_reshaper.reshape(segment)
                    processed_segment = get_display(reshaped)
                else:
                    processed_segment = segment
                processed_segments.append((script, processed_segment))
            
            processed_lines.append(processed_segments)
        
        return processed_lines

    def execute(self, **kwargs):
        text = kwargs.get("Text", "سلام کامفی")
        farsi_font = kwargs.get("Farsi/Arabic Font", "BYekan.ttf")
        latin_font = kwargs.get("English/Latin Font", "arial.ttf")
        size = kwargs.get("Size", 60)
        text_color = kwargs.get("Text Color", "Black")
        background_color = kwargs.get("Background Color", "White")
        horizontal_align = kwargs.get("Horizontal Align", "center")
        vertical_align = kwargs.get("Vertical Align", "center")
        image_width = kwargs.get("Image Width", 512)
        image_height = kwargs.get("Image Height", 512)
        rotation = kwargs.get("Rotation", 0.0)
        offset_x = kwargs.get("Offset X", 0)
        offset_y = kwargs.get("Offset Y", 0)
        shadow_distance = kwargs.get("Shadow Distance", 0)
        shadow_blur = kwargs.get("Shadow Blur", 0)
        shadow_color = kwargs.get("Shadow Color", "Black")
        text_color_hex = kwargs.get("Text Color Hex", "#000000")
        background_color_hex = kwargs.get("Background Color Hex", "#FFFFFF")
        shadow_color_hex = kwargs.get("Shadow Color Hex", "#000000")
        padding = kwargs.get("Padding", 0)
        transparent_background = kwargs.get("Transparent Background", False)

        # Validate and process HEX colors
        def validate_hex_color(hex_str, default_rgb):
            if not hex_str or not isinstance(hex_str, str):
                return default_rgb
            hex_str = hex_str.strip()
            # Remove leading '#' if present
            hex_str = hex_str.lstrip('#')
            # Check if the string is a valid HEX color (6 or 8 characters)
            if re.match(r'^[0-9a-fA-F]{6}$|^[0-9a-fA-F]{8}$', hex_str):
                try:
                    return ImageColor.getrgb(f"#{hex_str}")
                except ValueError:
                    return default_rgb
            return default_rgb

        # Assign colors with validation
        text_rgb = color_mapping.get(text_color, (0, 0, 0)) if text_color != "Custom (HEX Color)" else validate_hex_color(text_color_hex, (0, 0, 0))
        background_rgb = color_mapping.get(background_color, (255, 255, 255)) if background_color != "Custom (HEX Color)" else validate_hex_color(background_color_hex, (255, 255, 255))
        shadow_rgb = color_mapping.get(shadow_color, (0, 0, 0)) if shadow_color != "Custom (HEX Color)" else validate_hex_color(shadow_color_hex, (0, 0, 0))

        font_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Fonts")
        farsi_font_path = os.path.join(font_dir, "arial.ttf" if farsi_font == "default" else farsi_font)
        latin_font_path = os.path.join(font_dir, "arial.ttf" if latin_font == "default" else latin_font)

        try:
            arabic_selected_font = ImageFont.truetype(farsi_font_path, size)
            latin_selected_font = ImageFont.truetype(latin_font_path, size)
        except Exception as e:
            raise ValueError(f"Failed to load fonts: {str(e)}")

        processed_lines = self.process_text(text, "auto")

        # Initialize background and mask layer
        background = Image.new("RGBA", (image_width, image_height), background_rgb + (255,) if not transparent_background else (0, 0, 0, 0))
        mask_layer = Image.new("L", (image_width, image_height), 0)
        mask_draw = ImageDraw.Draw(mask_layer)

        # Calculate text dimensions and positions
        padded_width = image_width - 2 * padding
        padded_height = image_height - 2 * padding
        line_heights = []
        segment_widths = []
        segment_fonts = []
        for line in processed_lines:
            max_height = 0
            line_width = 0
            line_segment_widths = []
            line_segment_fonts = []
            for j, (script, segment) in enumerate(line):
                selected_font = arabic_selected_font if script == "arabic" else latin_selected_font
                bbox = selected_font.getbbox(segment)
                segment_width = bbox[2] - bbox[0]
                line_segment_widths.append(segment_width)
                line_segment_fonts.append(selected_font)
                line_width += segment_width
                max_height = max(max_height, bbox[3] - bbox[1])
                if j < len(line) - 1:
                    line_width += 10
            line_heights.append(max_height)
            segment_widths.append(line_segment_widths)
            segment_fonts.append(line_segment_fonts)
        total_text_height = sum(line_heights) + 10 * (len(processed_lines) - 1)

        # Vertical alignment
        if vertical_align == "top":
            y_start = padding + offset_y
        elif vertical_align == "bottom":
            y_start = image_height - padding - total_text_height + offset_y
        else:
            y_start = (image_height - total_text_height) // 2 + offset_y

        # Draw text on mask_layer
        y = y_start
        for i, line in enumerate(processed_lines):
            if not line:
                y += line_heights[i] + 10
                continue

            line_width = sum(segment_widths[i]) + 10 * (len(line) - 1)
            
            rtl_chars = sum(len(seg) for script, seg in line if script == "arabic")
            total_chars = sum(len(seg) for script, seg in line)
            is_rtl_line = rtl_chars > total_chars / 2

            if horizontal_align == "left":
                x_start = padding + offset_x
            elif horizontal_align == "center":
                x_start = (padded_width - line_width) // 2 + offset_x
            else:
                x_start = padded_width - line_width - padding + offset_x

            if is_rtl_line:
                current_x = x_start + line_width
            else:
                current_x = x_start

            line_segments = reversed(line) if is_rtl_line else line
            segment_widths_for_line = reversed(segment_widths[i]) if is_rtl_line else segment_widths[i]
            segment_fonts_for_line = reversed(segment_fonts[i]) if is_rtl_line else segment_fonts[i]

            for (script, segment), segment_width, selected_font in zip(line_segments, segment_widths_for_line, segment_fonts_for_line):
                spacing = 10 if len(line) > 1 else 0
                
                if is_rtl_line:
                    draw_x = current_x - segment_width
                else:
                    draw_x = current_x

                mask_draw.text(
                    (draw_x, y),
                    segment,
                    font=selected_font,
                    fill=255
                )

                if is_rtl_line:
                    current_x -= (segment_width + spacing)
                else:
                    current_x += (segment_width + spacing)

            y += line_heights[i] + 10

        # Apply shadow if enabled
        if shadow_distance > 0 or shadow_blur > 0:
            shadow_mask = Image.new("L", background.size, 0)
            offset_x_shadow = int(shadow_distance)
            offset_y_shadow = int(shadow_distance)
            # Paste mask_layer at offset for shadow
            shadow_mask.paste(mask_layer, (offset_x_shadow, offset_y_shadow))
            if shadow_blur > 0:
                shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(shadow_blur))
            shadow_layer = Image.new("RGBA", background.size, shadow_rgb + (255,))
            shadow_layer.putalpha(shadow_mask)
            background = Image.alpha_composite(background, shadow_layer)

        # Apply text layer
        text_layer = Image.new("RGBA", background.size, text_rgb + (255,))
        text_layer.putalpha(mask_layer)
        background = Image.alpha_composite(background, text_layer)

        # Apply rotation
        if rotation != 0:
            fill_color = background_rgb + (255,) if not transparent_background else (0, 0, 0, 0)
            background = background.rotate(rotation, expand=False, fillcolor=fill_color)
            mask_layer = mask_layer.rotate(rotation, expand=False, fillcolor=0)

        # Convert to tensors
        image_np = np.array(background).astype(np.float32) / 255.0
        mask_np = np.array(mask_layer).astype(np.float32) / 255.0

        return (torch.from_numpy(image_np).unsqueeze(0), torch.from_numpy(mask_np).unsqueeze(0))

NODE_CLASS_MAPPINGS = {
    "PersianText": PersianText
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PersianText": "Persian Text Generator"
}
