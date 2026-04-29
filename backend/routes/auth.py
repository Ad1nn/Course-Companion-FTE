from fastapi import APIRouter, HTTPException, status
from database import supabase
from models import AuthRegisterRequest, AuthLoginRequest, AuthRegisterResponse, AuthLoginResponse

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
    try:
        result = supabase.auth.sign_in_with_password({"email": body.email, "password": body.password})
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not result.user or not result.session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user_id = result.user.id
    access_token = result.session.access_token

    user_result = supabase.table("users").select("tier").eq("id", user_id).single().execute()
    tier = user_result.data["tier"] if user_result.data else "free"

    return AuthLoginResponse(access_token=access_token, user_id=user_id, tier=tier)
