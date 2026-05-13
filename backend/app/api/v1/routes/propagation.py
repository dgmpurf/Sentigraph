from fastapi import APIRouter

from app.schemas.propagation import PropagationResponse
from app.services.mock_service import get_mock_propagation

router = APIRouter()


@router.get("/{project_id}", response_model=PropagationResponse)
def get_propagation(project_id: str) -> PropagationResponse:
    return get_mock_propagation(project_id)

