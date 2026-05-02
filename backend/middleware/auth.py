from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from database import supabase
from models import AuthUser

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> AuthUser:
    token = credentials.credentials
    try:
        response = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    if not response or not response.user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = response.user.id

    try:
        result = supabase.table("users").select("tier").eq("id", user_id).maybe_single().execute()
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    if not result or not result.data:
        # Auth token is valid but no profile row — auto-create with free tier
        try:
            supabase.table("users").insert({
                "id": user_id,
                "email": response.user.email,
                "tier": "free",
            }).execute()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user profile")
        return AuthUser(user_id=user_id, tier="free")

    return AuthUser(user_id=user_id, tier=result.data["tier"])
