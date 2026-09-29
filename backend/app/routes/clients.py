from fastapi import APIRouter, HTTPException
from typing import List
from ..schemas.client import ClientSummary, ClientDetail
from ..services.meeting_service import meeting_service

router = APIRouter(prefix="/api/clients", tags=["Clients"])


@router.get("", response_model=List[ClientSummary], summary="List All Tracked Clients")
def list_clients() -> List[ClientSummary]:
    """
    Returns high-level summary of all clients tracked in RecallMeet AI.
    """
    return meeting_service.get_clients()


@router.get("/{client}", response_model=ClientDetail, summary="Get Client Intelligence Profile")
def get_client(client: str) -> ClientDetail:
    """
    Retrieves deep profile for a client derived from meeting history and Hindsight memories.
    """
    detail = meeting_service.get_client_detail(client)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Client '{client}' not found.")
    return detail
