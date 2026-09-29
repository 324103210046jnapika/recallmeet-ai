from fastapi import APIRouter, HTTPException

from ..schemas.memory import MemoryRecallRequest, MemoryRecallResponse
from ..services.hindsight_service import hindsight_service


router = APIRouter(
    prefix="/api/memory",
    tags=["Memory (Hindsight)"]
)


@router.post(
    "/recall",
    response_model=MemoryRecallResponse,
    summary="Recall Client Memories from Hindsight"
)
async def recall_memory(
    request: MemoryRecallRequest
) -> MemoryRecallResponse:
    """
    Directly query Hindsight memory bank for semantic and episodic client memories.

    Uses multi-strategy recall:
    - facts
    - entities
    - experiences
    - temporal reasoning

    Explicitly reports memory_provider:
    - hindsight
    - local_fallback
    """
    try:
        memories, provider_name, op_info = (
            await hindsight_service.recall_memories(
                client=request.client,
                query=request.query,
                bank_id=request.bank_id
            )
        )

        hindsight_info = await hindsight_service.check_connection()
        connected = hindsight_info.get("connected", False)

        if provider_name == "hindsight":
            status_msg = (
                f"Successfully recalled {len(memories)} memories "
                f"directly from Hindsight memory engine "
                f"(bank: '{op_info.bank_id}')"
            )
        else:
            status_msg = (
                f"Recalled {len(memories)} memories from "
                f"development fallback layer "
                f"(Hindsight server offline)"
            )

        return MemoryRecallResponse(
            client=request.client,
            query=request.query,
            total_recalled=len(memories),
            memories=memories,
            hindsight_connected=connected,
            status_message=status_msg,
            memory_provider=provider_name,
            memory_info=op_info
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Memory recall error: {str(e)}"
        )