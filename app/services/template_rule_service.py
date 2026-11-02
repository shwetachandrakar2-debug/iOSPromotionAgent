from app.schemas.campaign import CampaignRequestSchema, AIAgentStructuredDecision


class TemplateRuleService:
    """Deterministic, zero-token fallback engine generating rule-based ad copy."""

    @staticmethod
    def generate_fallback_strategy(request: CampaignRequestSchema) -> AIAgentStructuredDecision:
        biz = request.business
        offer = request.offer_headline

        if request.language.lower() == "hinglish":
            headline = f"Iss Weekend, {offer}!"
            body = (
                f"Tyohar aur celebrations ka mausam shuru! Apne style ko revamp karein at {biz.name}. "
                f"Paiye {offer}! Slots tezi se fill ho rahe hain."
            )
            cta = f"WhatsApp par 'OFFER' likh kar send karein: {biz.whatsapp}"
        else:
            headline = f"Exclusive: {offer}!"
            body = (
                f"Upgrade your look at {biz.name}! "
                f"Enjoy {offer} across all services. Hurry, book your slot today!"
            )
            cta = f"Book instantly via WhatsApp: {biz.whatsapp}"

        hashtags = [
            f"#{biz.category.replace(' ', '')}",
            f"#{biz.city}Deals",
            "#SpecialDiscount",
            "#LocalBusiness",
        ]

        return AIAgentStructuredDecision(
            marketing_angle="Template Fallback Rule",
            headline=headline,
            body_caption=body,
            cta_whatsapp=cta,
            hashtags=hashtags,
            primary_color_hex="#ED8936"
        )
