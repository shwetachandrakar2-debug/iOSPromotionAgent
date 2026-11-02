from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ExecutionModeEnum(str, Enum):
    AI_AGENT = "AI_AGENT"
    TEMPLATE_RULE = "TEMPLATE_RULE"


class ColorPaletteEnum(str, Enum):
    GOLD_DARK = "gold_dark"
    CRIMSON = "crimson"
    TEAL = "teal"


class BusinessProfileSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=120, example="Royal Unisex Salon")
    phone: str = Field(..., pattern=r"^[+]?[0-9\s-]{8,20}$", example="+91 98765 43210")
    whatsapp: str = Field(..., pattern=r"^[+]?[0-9\s-]{8,20}$", example="+91 98765 43210")
    category: str = Field("Salon & Spa", max_length=60, example="Salon & Spa")
    city: str = Field("Raipur", max_length=60, example="Raipur")


class CampaignRequestSchema(BaseModel):
    business: BusinessProfileSchema
    objective: str = Field("Drive WhatsApp Inquiries", example="Drive WhatsApp Inquiries")
    offer_headline: str = Field("Flat 35% OFF on Keratin & Hair Spa", min_length=3, max_length=150)
    language: str = Field("hinglish", example="hinglish")
    execution_mode: ExecutionModeEnum = Field(default=ExecutionModeEnum.AI_AGENT)
    theme_palette: ColorPaletteEnum = Field(default=ColorPaletteEnum.GOLD_DARK)


class AIAgentStructuredDecision(BaseModel):
    marketing_angle: str = Field(description="Psychological angle used, e.g., Festive Urgency, Luxury")
    headline: str = Field(description="Catchy punchy headline under 7 words")
    body_caption: str = Field(description="Bilingual high-conversion social caption")
    cta_whatsapp: str = Field(description="WhatsApp trigger with keyword instruction")
    hashtags: List[str] = Field(description="4-5 trending niche tags")
    primary_color_hex: str = Field(default="#ED8936", description="Hex color matching theme")


class CampaignResponseSchema(BaseModel):
    status: str = "success"
    mode_used: ExecutionModeEnum
    headline: str
    body_caption: str
    cta_whatsapp: str
    hashtags: List[str]
    poster_base64: str
