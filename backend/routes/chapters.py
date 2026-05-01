from fastapi import APIRouter, Depends, HTTPException, status
from database import supabase
from middleware.auth import get_current_user
from models import AuthUser, ChapterSummary, ChapterDetail, TIER_ORDER

router = APIRouter()


def _check_tier_access(chapter: dict, user: AuthUser):
    if TIER_ORDER[user.tier] < TIER_ORDER.get(chapter["tier"], 0):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "detail": "Access denied",
                "required_tier": chapter["tier"],
                "user_tier": user.tier,
                "message": f"Chapter '{chapter['title']}' requires a {chapter['tier'].capitalize()} subscription.",
            },
        )


@router.get("", response_model=list[ChapterSummary])
def list_chapters(user: AuthUser = Depends(get_current_user)):
    result = supabase.table("chapters").select("id, title, description, order_num, tier").order("order_num").execute()
    return result.data or []


@router.get("/{chapter_id}", response_model=ChapterDetail)
def get_chapter(chapter_id: int, user: AuthUser = Depends(get_current_user)):
    result = supabase.table("chapters").select("*").eq("id", chapter_id).maybe_single().execute()
    if not result or not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")
    chapter = result.data
    _check_tier_access(chapter, user)
    return chapter


@router.get("/{chapter_id}/next", response_model=ChapterSummary)
def get_next_chapter(chapter_id: int, user: AuthUser = Depends(get_current_user)):
    current = supabase.table("chapters").select("order_num").eq("id", chapter_id).maybe_single().execute()
    if not current or not current.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")
    result = (
        supabase.table("chapters")
        .select("id, title, description, order_num, tier")
        .gt("order_num", current.data["order_num"])
        .order("order_num")
        .limit(1)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No next chapter")
    return result.data[0]


@router.get("/{chapter_id}/prev", response_model=ChapterSummary)
def get_prev_chapter(chapter_id: int, user: AuthUser = Depends(get_current_user)):
    current = supabase.table("chapters").select("order_num").eq("id", chapter_id).maybe_single().execute()
    if not current or not current.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")
    result = (
        supabase.table("chapters")
        .select("id, title, description, order_num, tier")
        .lt("order_num", current.data["order_num"])
        .order("order_num", desc=True)
        .limit(1)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No previous chapter")
    return result.data[0]
