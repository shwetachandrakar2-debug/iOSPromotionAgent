from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.campaign import CampaignRequestSchema, CampaignResponseSchema
from app.services.orchestration_service import CampaignOrchestrationService

router = APIRouter(prefix="/campaign", tags=["Campaigns"])


def get_orchestrator_service() -> CampaignOrchestrationService:
    return CampaignOrchestrationService()


@router.post(
    "/orchestrate",
    response_model=CampaignResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Generate social media campaign & poster"
)
async def orchestrate_campaign_endpoint(
    payload: CampaignRequestSchema,
    service: CampaignOrchestrationService = Depends(get_orchestrator_service)
) -> CampaignResponseSchema:
    try:
        return service.process_campaign(payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Campaign orchestration failed: {str(e)}"
        )
