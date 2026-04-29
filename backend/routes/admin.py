import os
from fastapi import APIRouter, Header, HTTPException, status
from database import supabase
from models import AdminUpgradeRequest

router = APIRouter()

VALID_TIERS = {"free", "premium", "pro"}


@router.post("/upgrade")
def upgrade_user(
    body: AdminUpgradeRequest,
    admin_secret: str = Header(None, alias="ADMIN_SECRET"),
):
    expected = os.environ.get("ADMIN_SECRET", "")
    if not admin_secret or admin_secret != expected:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing ADMIN_SECRET")

    if body.tier not in VALID_TIERS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Tier must be one of: {VALID_TIERS}")

    result = supabase.table("users").update({"tier": body.tier}).eq("id", body.user_id).execute()
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"message": f"User upgraded to {body.tier}"}
