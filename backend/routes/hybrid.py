import json
import os
from datetime import datetime, timezone

from openai import OpenAI
from fastapi import APIRouter, Depends, HTTPException, status

from database import supabase
from middleware.auth import get_current_user
from models import (
    AdaptivePathRequest,
    AdaptivePathResponse,
    AssessRequest,
    AssessResponse,
    AuthUser,
)

router = APIRouter()

_openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
_MODEL = "gpt-4o"


def _require_pro(user: AuthUser) -> None:
    if user.tier != "pro":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This feature requires a Pro subscription.",
        )


def _log_cost(user_id: str, feature: str, tokens_in: int, tokens_out: int) -> None:
    # gpt-4o: $2.50/1M input, $10/1M output
    cost = (tokens_in / 1_000_000) * 2.50 + (tokens_out / 1_000_000) * 10.0
    try:
        supabase.table("llm_costs").insert({
            "user_id": user_id,
            "feature": feature,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "cost_usd": round(cost, 6),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }).execute()
    except Exception:
        pass  # cost logging is non-critical


def _parse_json(text: str) -> dict:
    # Strip markdown fences if present
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        text = text.rsplit("```", 1)[0]
    return json.loads(text.strip())


@router.post("/adaptive-path", response_model=AdaptivePathResponse)
def adaptive_path(body: AdaptivePathRequest, user: AuthUser = Depends(get_current_user)):
    _require_pro(user)

    ch_result = supabase.table("chapters").select("id, title, description, order_num, tier").order("order_num").execute()
    chapters = ch_result.data or []

    prog_result = (
        supabase.table("progress")
        .select("chapter_id, completed, score, attempts")
        .eq("user_id", body.user_id)
        .execute()
    )
    progress = prog_result.data or []

    completed_ids = {p["chapter_id"] for p in progress if p["completed"]}
    incomplete_chapters = [c for c in chapters if c["id"] not in completed_ids]

    if not incomplete_chapters:
        scored = [(p["chapter_id"], p["score"] or 0) for p in progress if p["score"] is not None]
        worst_id = min(scored, key=lambda x: x[1])[0] if scored else (chapters[0]["id"] if chapters else 1)
        incomplete_chapters = [c for c in chapters if c["id"] == worst_id] or chapters[:1]

    progress_summary = "\n".join(
        f"- Chapter {p['chapter_id']}: {'completed' if p['completed'] else 'incomplete'}, "
        f"score={p['score']}, attempts={p['attempts']}"
        for p in progress
    ) or "No progress recorded yet."

    chapters_list = "\n".join(
        f"- id={c['id']}, title={c['title']!r}, order={c['order_num']}, tier={c['tier']}"
        for c in chapters
    )

    prompt = f"""You are an adaptive learning coach for a course on Agentic AI development.

Available chapters:
{chapters_list}

Student progress:
{progress_summary}

Incomplete chapters (candidates to recommend):
{json.dumps([{"id": c["id"], "title": c["title"], "order_num": c["order_num"]} for c in incomplete_chapters], indent=2)}

Based on the student's progress, recommend the single best next chapter to study.
Identify weak areas from low scores or incomplete chapters.
Estimate realistic study time in minutes (20–120).

Respond with ONLY a JSON object (no markdown fences):
{{
  "recommended_next_chapter_id": <integer>,
  "reasoning": "<1-2 sentence explanation>",
  "weak_areas": ["<topic>", ...],
  "estimated_study_time_minutes": <integer>
}}"""

    response = _openai.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.3,
    )

    usage = response.usage
    _log_cost(body.user_id, "adaptive-path", usage.prompt_tokens, usage.completion_tokens)

    try:
        data = _parse_json(response.choices[0].message.content)
        return AdaptivePathResponse(**data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to parse LLM response.",
        )


@router.post("/assess", response_model=AssessResponse)
def assess(body: AssessRequest, user: AuthUser = Depends(get_current_user)):
    _require_pro(user)

    ch_result = (
        supabase.table("chapters")
        .select("title, description")
        .eq("id", body.chapter_id)
        .maybe_single()
        .execute()
    )
    chapter = ch_result.data or {}
    chapter_title = chapter.get("title", f"Chapter {body.chapter_id}")
    chapter_desc = chapter.get("description", "")

    prompt = f"""You are an expert tutor grading a student's answer for a course on Agentic AI development.

Chapter: {chapter_title}
{f'Topic: {chapter_desc}' if chapter_desc else ''}

Question asked:
{body.question}

Student's answer:
{body.answer}

Evaluate the answer thoroughly and fairly. Score from 0 to 100.

Respond with ONLY a JSON object (no markdown fences):
{{
  "score": <integer 0-100>,
  "feedback": "<2-3 sentence overall feedback>",
  "strengths": ["<specific strength>", ...],
  "areas_to_improve": ["<specific gap or misconception>", ...]
}}"""

    response = _openai.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.3,
    )

    usage = response.usage
    _log_cost(body.user_id, "assess", usage.prompt_tokens, usage.completion_tokens)

    try:
        data = _parse_json(response.choices[0].message.content)
        return AssessResponse(**data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to parse LLM response.",
        )
