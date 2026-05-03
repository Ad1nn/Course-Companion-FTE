from fastapi import APIRouter, Depends, HTTPException, status
from supabase import create_client
from database import supabase, SUPABASE_URL, SUPABASE_SERVICE_KEY
from middleware.auth import get_current_user
from models import AuthRegisterRequest, AuthLoginRequest, AuthRegisterResponse, AuthLoginResponse, AuthUser
from pydantic import BaseModel

router = APIRouter()


@router.post("/register", response_model=AuthRegisterResponse)
def register(body: AuthRegisterRequest):
    try:
        # Use admin API to bypass email confirmation and rate limits
        result = supabase.auth.admin.create_user({
            "email": body.email,
            "password": body.password,
            "email_confirm": True,
        })
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not result.user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Registration failed")

    user_id = result.user.id
    email = result.user.email

    # Insert into users table
    try:
        supabase.table("users").insert({"id": user_id, "email": email, "tier": "free"}).execute()
    except Exception:
        # Clean up auth user if users insert fails
        supabase.auth.admin.delete_user(user_id)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user profile")

    return AuthRegisterResponse(user_id=user_id, email=email, tier="free")


@router.post("/login", response_model=AuthLoginResponse)
def login(body: AuthLoginRequest):
    # Use an isolated client so sign_in_with_password never overwrites the
    # service-role singleton's Authorization header (which would flip all
    # subsequent PostgREST queries from service_role → authenticated role,
    # causing RLS to block every table query).
    try:
        _auth = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        result = _auth.auth.sign_in_with_password({"email": body.email, "password": body.password})
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not result.user or not result.session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user_id = result.user.id
    access_token = result.session.access_token

    user_result = supabase.table("users").select("tier").eq("id", user_id).maybe_single().execute()
    tier = user_result.data["tier"] if (user_result and user_result.data) else "free"

    return AuthLoginResponse(access_token=access_token, user_id=user_id, tier=tier)


class UpgradeTierRequest(BaseModel):
    tier: str  # 'premium' | 'pro'


@router.post("/upgrade-tier")
def upgrade_tier(body: UpgradeTierRequest, user: AuthUser = Depends(get_current_user)):
    if body.tier not in ("premium", "pro"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid tier. Must be 'premium' or 'pro'.")
    supabase.table("users").update({"tier": body.tier}).eq("id", user.user_id).execute()
    return {"user_id": user.user_id, "tier": body.tier}
