import os
import torch
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageFilter
from arabic_reshaper import reshape
from torchvision.transforms.functional import to_tensor
import numpy as np
from .utils.colors import COLORS, color_mapping


class PersianText:
    @classmethod
    def INPUT_TYPES(s):
        
        fonts_dir = os.path.join(os.path.dirname(__file__), "Fonts")
        available_fonts = [f for f in os.listdir(fonts_dir) if f.endswith('.ttf')]

        return {
            "required": {
                "text": ("STRING", {"multiline": True, "dynamicPrompts": True, "default": "سلام کامفی"}),
                "font": (available_fonts, {"default": available_fonts[0] if available_fonts else "BYekan.ttf"}),
                "size": ("INT", {"default": 60, "min": 1, "max": 9999, "step": 1}),
                "text_color": (COLORS, {"default": "black"}),
                "background_color": (COLORS, {"default": "white"}),
                "horizontal_align": (["left", "center", "right"], {"default": "center"}),
                "vertical_align": (["top", "center", "bottom"], {"default": "center"}),
                "image_width": ("INT", {"default": 512, "min": 1, "max": 4096, "step": 1}),
                "image_height": ("INT", {"default": 512, "min": 1, "max": 4096, "step": 1}),
                "rotation": ("FLOAT", {"default": 0.0, "min": -360, "max": 360, "step": 0.1}),
                "offset_x": ("INT", {"default": 0, "min": -4096, "max": 4096, "step": 1}),
                "offset_y": ("INT", {"default": 0, "min": -4096, "max": 4096, "step": 1}),
                "shadow_distance": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1}),
                "shadow_blur": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1}),
                "shadow_color": (COLORS, {"default": "black"}),
                "direction": (["LTR", "RTL"], {"default": "RTL"}),
            },
            "optional": {
                "text_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                "background_color_hex": ("STRING", {"multiline": False, "default": "#FFFFFF"}),
                "shadow_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "execute"
    CATEGORY = "🎨KG"

    def process_text(self, text, direction):
        
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

    def get_color_values(self, color_name, hex_color):
        
        if color_name == "custom" and hex_color.startswith("#"):
            try:
                return ImageColor.getrgb(hex_color)
            except ValueError:
                pass
        return color_mapping.get(color_name, (0, 0, 0))  # default black

    def execute(
        self, text, font, size, text_color, background_color, horizontal_align, vertical_align, image_width,
        image_height, rotation, offset_x, offset_y, shadow_distance, shadow_blur, shadow_color, direction,
        text_color_hex="#000000",
        background_color_hex="#FFFFFF",
        shadow_color_hex="#000000"
    ):
       
        # Process text (RTL or LTR)
        bidi_text = self.process_text(text, direction)

        # Load font
        fonts_dir = os.path.join(os.path.dirname(__file__), "Fonts")
        font_path = os.path.join(fonts_dir, font)
        try:
            selected_font = ImageFont.truetype(font_path, size)
        except IOError:
            selected_font = ImageFont.load_default()

        # Convert color inputs
        text_rgb = self.get_color_values(text_color, text_color_hex)
        background_rgb = self.get_color_values(background_color, background_color_hex)
        shadow_rgb = self.get_color_values(shadow_color, shadow_color_hex)

        background_image = Image.new('RGB', (image_width, image_height), background_rgb)

        lines = bidi_text.split('\n')

        line_heights = [selected_font.getbbox(ln)[3] for ln in lines if ln.strip()]
        if line_heights:
            total_height = sum(line_heights) + (len(lines) - 1) * (selected_font.getbbox('A')[3] // 2)
        else:
            total_height = 0

        y_start = {
            "top": 0,
            "center": (image_height - total_height) // 2,
            "bottom": image_height - total_height
        }[vertical_align] + offset_y

        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')

        current_y = y_start

        # Precompute line positions
        line_positions = []  # List of (line_str, text_x, text_y, shadow_x, shadow_y)
        for line in lines:
            if not line.strip():
                # empty line => just add spacing
                current_y += selected_font.getbbox('A')[3] // 2
                continue

            # measure width/height
            line_bbox = selected_font.getbbox(line)  # (x0, y0, x1, y1)
            line_width = line_bbox[2]
            line_height = line_bbox[3]

            # horizontal alignment
            if horizontal_align == "left":
                text_x = 0
            elif horizontal_align == "center":
                text_x = (image_width - line_width) // 2
            else:  # "right"
                text_x = image_width - line_width

            text_x += offset_x
            text_y = current_y

            shadow_x = text_x + shadow_distance
            shadow_y = text_y + shadow_distance

            t_left   = text_x
            t_top    = text_y
            t_right  = text_x + line_width
            t_bottom = text_y + line_height

            min_x = min(min_x, t_left)
            min_y = min(min_y, t_top)
            max_x = max(max_x, t_right)
            max_y = max(max_y, t_bottom)

            if shadow_distance > 0:
                s_left   = shadow_x
                s_top    = shadow_y
                s_right  = shadow_x + line_width
                s_bottom = shadow_y + line_height
                min_x = min(min_x, s_left)
                min_y = min(min_y, s_top)
                max_x = max(max_x, s_right)
                max_y = max(max_y, s_bottom)

            line_positions.append((line, text_x, text_y, shadow_x, shadow_y, line_width, line_height))

            current_y += line_height + (selected_font.getbbox('A')[3] // 2)

        if not line_positions:
            image_np = np.array(background_image).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(image_np).unsqueeze(0)
            blank_mask = Image.new('L', (image_width, image_height), 0)
            mask_np = np.array(blank_mask).astype(np.float32) / 255.0
            mask_tensor = torch.from_numpy(mask_np).unsqueeze(0)
            return (image_tensor, mask_tensor)

        min_x, min_y = int(min_x), int(min_y)
        max_x, max_y = int(max_x), int(max_y)

        text_bbox_w = max_x - min_x
        text_bbox_h = max_y - min_y

        text_layer = Image.new('RGBA', (text_bbox_w, text_bbox_h), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_layer)

        if shadow_distance > 0:
            shadow_image = Image.new('RGBA', (text_bbox_w, text_bbox_h), (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow_image)

            for (line, tx, ty, sx, sy, w, h) in line_positions:
                if not line.strip():
                    continue
                shadow_draw.text(
                    (sx - min_x, sy - min_y),
                    line,
                    font=selected_font,
                    fill=shadow_rgb
                )

            shadow_image = shadow_image.filter(ImageFilter.GaussianBlur(shadow_blur))
            text_layer.alpha_composite(shadow_image)

        # Draw main text
        for (line, tx, ty, sx, sy, w, h) in line_positions:
            if not line.strip():
                continue
            text_draw.text(
                (tx - min_x, ty - min_y),
                line,
                font=selected_font,
                fill=text_rgb
            )

        if rotation != 0:
            text_layer = text_layer.rotate(rotation, expand=True)

        rotated_w, rotated_h = text_layer.size
        background_image.paste(text_layer, (min_x, min_y), text_layer)

        mask_layer = Image.new('L', (text_bbox_w, text_bbox_h), 0)
        mask_draw = ImageDraw.Draw(mask_layer)

        for (line, tx, ty, sx, sy, w, h) in line_positions:
            if not line.strip():
                continue
            mask_draw.text(
                (tx - min_x, ty - min_y),
                line,
                font=selected_font,
                fill=255
            )

        if rotation != 0:
            mask_layer = mask_layer.rotate(rotation, expand=True)

        final_mask = Image.new('L', (image_width, image_height), 0)
        final_mask.paste(mask_layer, (min_x, min_y), mask_layer)

        image_np = np.array(background_image).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np).unsqueeze(0)

        mask_np = np.array(final_mask).astype(np.float32) / 255.0
        mask_tensor = torch.from_numpy(mask_np).unsqueeze(0)

        return (image_tensor, mask_tensor)
