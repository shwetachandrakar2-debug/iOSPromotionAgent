import io
import base64
from typing import Dict, Any, Tuple
from PIL import Image, ImageDraw, ImageFont
from app.core.config import settings
from app.schemas.campaign import BusinessProfileSchema, ColorPaletteEnum


class PosterRenderService:
    """Responsible for rendering production-ready social media poster graphics with Pillow."""

    PALETTES: Dict[str, Dict[str, Tuple[int, int, int]]] = {
        ColorPaletteEnum.GOLD_DARK.value: {
            "bg": (15, 17, 26),
            "card": (26, 32, 44),
            "accent": (237, 137, 54),
            "text": (255, 255, 255),
            "subtext": (160, 174, 192),
        },
        ColorPaletteEnum.CRIMSON.value: {
            "bg": (26, 12, 18),
            "card": (45, 18, 28),
            "accent": (245, 101, 101),
            "text": (255, 255, 255),
            "subtext": (203, 213, 225),
        },
        ColorPaletteEnum.TEAL.value: {
            "bg": (10, 25, 30),
            "card": (18, 42, 50),
            "accent": (56, 178, 172),
            "text": (255, 255, 255),
            "subtext": (160, 174, 192),
        },
    }

    def __init__(self, width: int = None, height: int = None):
        self.width = width or settings.DEFAULT_IMAGE_WIDTH
        self.height = height or settings.DEFAULT_IMAGE_HEIGHT

    def render_poster(
        self,
        business: BusinessProfileSchema,
        headline: str,
        palette_choice: str = ColorPaletteEnum.GOLD_DARK.value,
        accent_override_hex: str = None,
    ) -> str:
        theme = self.PALETTES.get(palette_choice, self.PALETTES[ColorPaletteEnum.GOLD_DARK.value]).copy()
        
        if accent_override_hex and accent_override_hex.startswith("#") and len(accent_override_hex) == 7:
            try:
                r = int(accent_override_hex[1:3], 16)
                g = int(accent_override_hex[3:5], 16)
                b = int(accent_override_hex[5:7], 16)
                theme["accent"] = (r, g, b)
            except ValueError:
                pass

        image = Image.new("RGB", (self.width, self.height), color=theme["bg"])
        draw = ImageDraw.Draw(image)

        try:
            font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 46)
            font_headline = ImageFont.truetype("DejaVuSans-Bold.ttf", 52)
            font_body = ImageFont.truetype("DejaVuSans.ttf", 32)
            font_footer = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
        except IOError:
            font_title = font_headline = font_body = font_footer = ImageFont.load_default()

        # Top Header
        draw.text((80, 80), business.name.upper(), fill=theme["accent"], font=font_title)
        draw.text((80, 140), f"{business.category} • {business.city}", fill=theme["subtext"], font=font_body)

        # Main Offer Graphic Card
        card_rect = [(80, 240), (self.width - 80, 840)]
        draw.rounded_rectangle(card_rect, radius=24, fill=theme["card"], outline=theme["accent"], width=3)

        # Offer Tag Badge
        draw.rounded_rectangle([(120, 290), (460, 350)], radius=8, fill=theme["accent"])
        draw.text((140, 305), "LIMITED TIME OFFER", fill=(255, 255, 255), font=font_footer)

        # Wrapped headline text
        words = headline.split(" ")
        lines = []
        curr = []
        for word in words:
            curr.append(word)
            if len(" ".join(curr)) > 20:
                lines.append(" ".join(curr[:-1]))
                curr = [word]
        if curr:
            lines.append(" ".join(curr))

        y = 400
        for line in lines:
            draw.text((120, y), line, fill=theme["text"], font=font_headline)
            y += 75

        draw.text((120, y + 30), "Transform your look today. Valid this week only!", fill=theme["subtext"], font=font_body)

        # Footer Contact Ribbon
        footer_height = 140
        draw.rectangle([(0, self.height - footer_height), (self.width, self.height)], fill=(10, 12, 16))
        contact_str = f"Call: {business.phone}   |   WhatsApp: {business.whatsapp}"
        draw.text((80, self.height - 85), contact_str, fill=(255, 255, 255), font=font_footer)

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=90)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
