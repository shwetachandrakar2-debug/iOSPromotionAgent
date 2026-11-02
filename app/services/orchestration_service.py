import logging
from app.schemas.campaign import (
    CampaignRequestSchema,
    CampaignResponseSchema,
    ExecutionModeEnum,
    AIAgentStructuredDecision
)
from app.services.ai_agent_service import AIAgentService
from app.services.template_rule_service import TemplateRuleService
from app.services.poster_render_service import PosterRenderService

logger = logging.getLogger(__name__)


class CampaignOrchestrationService:
    """Orchestrates strategy selection, copy creation, fallback execution, and poster rendering."""

    def __init__(
        self,
        ai_service: AIAgentService = None,
        template_service: TemplateRuleService = None,
        render_service: PosterRenderService = None
    ):
        self.ai_service = ai_service or AIAgentService()
        self.template_service = template_service or TemplateRuleService()
        self.render_service = render_service or PosterRenderService()

    def process_campaign(self, request: CampaignRequestSchema) -> CampaignResponseSchema:
        decision: AIAgentStructuredDecision = None
        mode_used = request.execution_mode

        if request.execution_mode == ExecutionModeEnum.AI_AGENT:
            try:
                decision = self.ai_service.generate_campaign_strategy(request)
            except Exception as e:
                logger.warning("AI Agent failed or unconfigured, gracefully falling back to Template Rule Engine. Error: %s", str(e))
                decision = self.template_service.generate_fallback_strategy(request)
                mode_used = ExecutionModeEnum.TEMPLATE_RULE
        else:
            decision = self.template_service.generate_fallback_strategy(request)

        # Render creative banner
        poster_b64 = self.render_service.render_poster(
            business=request.business,
            headline=decision.headline,
            palette_choice=request.theme_palette.value,
            accent_override_hex=decision.primary_color_hex
        )

        return CampaignResponseSchema(
            status="success",
            mode_used=mode_used,
            headline=decision.headline,
            body_caption=decision.body_caption,
            cta_whatsapp=decision.cta_whatsapp,
            hashtags=decision.hashtags,
            poster_base64=f"data:image/jpeg;base64,{poster_b64}"
        )
