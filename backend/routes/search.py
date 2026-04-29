from fastapi import APIRouter, Depends, HTTPException, status
from database import supabase
from middleware.auth import get_current_user
from models import AuthUser, SearchResult

router = APIRouter()

EXCERPT_LEN = 150


def _make_excerpt(content: str, keyword: str) -> str:
    idx = content.lower().find(keyword.lower())
    if idx == -1:
        return content[:EXCERPT_LEN] + "..."
    start = max(0, idx - 60)
    end = min(len(content), start + EXCERPT_LEN)
    excerpt = content[start:end]
    if start > 0:
        excerpt = "..." + excerpt
    if end < len(content):
        excerpt = excerpt + "..."
    return excerpt


@router.get("/search", response_model=list[SearchResult])
def search_chapters(q: str = "", user: AuthUser = Depends(get_current_user)):
    if not q.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Search query cannot be empty")

    title_results = (
        supabase.table("chapters")
        .select("id, title, content, tier")
        .ilike("title", f"%{q}%")
        .execute()
    )
    content_results = (
        supabase.table("chapters")
        .select("id, title, content, tier")
        .ilike("content", f"%{q}%")
        .execute()
    )

    seen = {}
    for row in (title_results.data or []) + (content_results.data or []):
        if row["id"] not in seen:
            seen[row["id"]] = row

    results = []
    for row in list(seen.values())[:5]:
        results.append(
            SearchResult(
                id=row["id"],
                title=row["title"],
                excerpt=_make_excerpt(row.get("content", ""), q),
                tier=row["tier"],
            )
        )
    return results
