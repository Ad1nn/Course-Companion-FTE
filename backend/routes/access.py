from fastapi import APIRouter, Depends, HTTPException, status
from database import supabase
from middleware.auth import get_current_user
from models import AuthUser, AccessCheckResponse, TIER_ORDER

router = APIRouter()


@router.get("/check", response_model=AccessCheckResponse)
def check_access(chapter_id: int, user: AuthUser = Depends(get_current_user)):
    result = supabase.table("chapters").select("tier").eq("id", chapter_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")

    chapter_tier = result.data["tier"]
    allowed = TIER_ORDER[user.tier] >= TIER_ORDER.get(chapter_tier, 0)

    if allowed:
        return AccessCheckResponse(allowed=True)
    return AccessCheckResponse(allowed=False, required_tier=chapter_tier, user_tier=user.tier)
