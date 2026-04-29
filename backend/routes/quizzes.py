from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from database import supabase
from middleware.auth import get_current_user
from models import AuthUser, QuizQuestion, SubmitRequest, SubmitResponse

router = APIRouter()

VALID_ANSWERS = {"A", "B", "C", "D"}


@router.get("/{chapter_id}", response_model=list[QuizQuestion])
def get_quiz_questions(chapter_id: int, user: AuthUser = Depends(get_current_user)):
    result = (
        supabase.table("quizzes")
        .select("id, chapter_id, question, option_a, option_b, option_c, option_d, order_num")
        .eq("chapter_id", chapter_id)
        .order("order_num")
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No questions found for this chapter")
    return result.data


@router.post("/{quiz_id}/submit", response_model=SubmitResponse)
def submit_answer(quiz_id: int, body: SubmitRequest, user: AuthUser = Depends(get_current_user)):
    if body.answer.upper() not in VALID_ANSWERS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Answer must be A, B, C, or D")

    question = supabase.table("quizzes").select("*").eq("id", quiz_id).single().execute()
    if not question.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    q = question.data
    is_correct = body.answer.upper() == q["correct_answer"]

    # Count total questions for this chapter
    all_questions = (
        supabase.table("quizzes")
        .select("id")
        .eq("chapter_id", q["chapter_id"])
        .execute()
    )
    total_questions = len(all_questions.data or [])

    # Count how many this user has answered for this chapter
    # We track answers via progress table — increment attempts as proxy
    progress_row = (
        supabase.table("progress")
        .select("*")
        .eq("user_id", body.user_id)
        .eq("chapter_id", q["chapter_id"])
        .execute()
    )

    score = None
    # If this is the final question (attempt count + 1 == total), calculate score
    current_attempts = progress_row.data[0]["attempts"] if progress_row.data else 0
    new_attempts = current_attempts + 1

    if new_attempts >= total_questions:
        # We approximate score: track correct submissions via a running total
        # For simplicity: fetch stored partial score or default, add current
        current_score_sum = progress_row.data[0].get("score") or 0
        if progress_row.data and progress_row.data[0].get("completed"):
            # Already completed — retake: reset
            current_score_sum = 0
            new_attempts = 1

        correct_count = current_score_sum + (1 if is_correct else 0)
        score = int((correct_count / total_questions) * 100)

        now = datetime.now(timezone.utc).isoformat()
        upsert_data = {
            "user_id": body.user_id,
            "chapter_id": q["chapter_id"],
            "completed": True,
            "score": score,
            "attempts": new_attempts,
            "last_accessed": now,
            "completed_at": now,
        }
    else:
        # Track running correct count in score field temporarily
        existing = progress_row.data[0] if progress_row.data else None
        current_correct = (existing.get("score") or 0) if existing and not existing.get("completed") else 0
        new_correct = current_correct + (1 if is_correct else 0)

        upsert_data = {
            "user_id": body.user_id,
            "chapter_id": q["chapter_id"],
            "completed": False,
            "score": new_correct,
            "attempts": new_attempts,
            "last_accessed": datetime.now(timezone.utc).isoformat(),
        }

    supabase.table("progress").upsert(upsert_data, on_conflict="user_id,chapter_id").execute()

    return SubmitResponse(
        correct=is_correct,
        correct_answer=q["correct_answer"],
        explanation=q["explanation"],
        score=score,
    )
