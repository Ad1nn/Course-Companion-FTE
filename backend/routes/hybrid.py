from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.post("/adaptive-path")
def adaptive_path():
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented — available in Phase 5")


@router.post("/assess")
def assess():
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented — available in Phase 5")
