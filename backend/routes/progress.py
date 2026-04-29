from datetime import datetime, timezone, date
from fastapi import APIRouter, Depends, HTTPException, status
from database import supabase
from middleware.auth import get_current_user
from models import AuthUser, ProgressResponse, ChapterProgress, ProgressUpdateRequest

router = APIRouter()


def _calculate_streak(completed_at_list: list[str]) -> int:
    if not completed_at_list:
        return 0
    dates = sorted(
        {datetime.fromisoformat(ts.replace("Z", "+00:00")).date() for ts in completed_at_list if ts},
        reverse=True,
    )
    if not dates:
        return 0
    today = datetime.now(timezone.utc).date()
    if dates[0] < today:
        return 0  # No activity today or yesterday resets streak
    streak = 1
    for i in range(1, len(dates)):
        if (dates[i - 1] - dates[i]).days == 1:
            streak += 1
        else:
            break
    return streak


@router.get("/{user_id}", response_model=ProgressResponse)
def get_progress(user_id: str, user: AuthUser = Depends(get_current_user)):
    user_row = supabase.table("users").select("tier").eq("id", user_id).single().execute()
    if not user_row.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    progress_rows = (
        supabase.table("progress")
        .select("chapter_id, completed, score, attempts, completed_at")
        .eq("user_id", user_id)
        .execute()
    )

    chapter_ids = [r["chapter_id"] for r in (progress_rows.data or [])]
    chapters_map = {}
    if chapter_ids:
        ch_result = supabase.table("chapters").select("id, title").in_("id", chapter_ids).execute()
        chapters_map = {c["id"]: c["title"] for c in (ch_result.data or [])}

    chapter_list = []
    completed_at_dates = []
    scores = []
    chapters_completed = 0

    for row in (progress_rows.data or []):
        chapter_list.append(
            ChapterProgress(
                chapter_id=row["chapter_id"],
                title=chapters_map.get(row["chapter_id"], ""),
                completed=row["completed"],
                score=row["score"] if row["completed"] else None,
                attempts=row["attempts"],
            )
        )
        if row["completed"]:
            chapters_completed += 1
            if row["score"] is not None:
                scores.append(row["score"])
            if row.get("completed_at"):
                completed_at_dates.append(row["completed_at"])

    avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0
    streak = _calculate_streak(completed_at_dates)

    return ProgressResponse(
        tier=user_row.data["tier"],
        streak_days=streak,
        avg_score=avg_score,
        chapters_completed=chapters_completed,
        chapters=chapter_list,
    )


@router.put("/{user_id}")
def update_progress(user_id: str, body: ProgressUpdateRequest, user: AuthUser = Depends(get_current_user)):
    now = datetime.now(timezone.utc).isoformat()
    upsert_data = {
        "user_id": user_id,
        "chapter_id": body.chapter_id,
        "completed": body.completed,
        "score": body.score,
        "last_accessed": now,
    }
    if body.completed:
        upsert_data["completed_at"] = now

    supabase.table("progress").upsert(upsert_data, on_conflict="user_id,chapter_id").execute()
    return {"message": "Progress updated"}
