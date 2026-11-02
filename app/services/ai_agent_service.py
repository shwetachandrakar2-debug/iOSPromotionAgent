import os
from typing import Tuple
from app.core.config import settings
from app.schemas.campaign import CampaignRequestSchema, AIAgentStructuredDecision

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


class AIAgentService:
    """Service responsible for interacting with LLM models for creative generation."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.client = None
        if genai and self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    def generate_campaign_strategy(self, request: CampaignRequestSchema) -> AIAgentStructuredDecision:
        if not self.client:
            raise RuntimeError("Gemini Client not initialized. GEMINI_API_KEY is missing or invalid.")

        prompt = f"""
        Act as an autonomous direct-response digital marketing agent for an Indian local small business.
        Business Details:
        - Name: {request.business.name}
        - Category: {request.business.category}
        - City: {request.business.city}
        - Offer/Promotion: {request.offer_headline}
        - Primary Objective: {request.objective}
        - Requested Language: {request.language} (if 'hinglish', write natural Hindi using English Latin alphabets).

        Generate an irresistible, high-converting offer copy package.
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AIAgentStructuredDecision,
                temperature=0.7,
            ),
        )

        return AIAgentStructuredDecision.model_validate_json(response.text)
