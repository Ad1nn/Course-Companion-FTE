from pydantic import BaseModel
from typing import Optional

# Tier hierarchy for access control
TIER_ORDER = {"free": 0, "premium": 1, "pro": 2}

# ── Chapter models ────────────────────────────────────────────────────────────

class ChapterSummary(BaseModel):
    id: int
    title: str
    description: Optional[str]
    order_num: int
    tier: str

class ChapterDetail(BaseModel):
    id: int
    title: str
    description: Optional[str]
    content: str
    order_num: int
    tier: str

# ── Quiz models ───────────────────────────────────────────────────────────────

class QuizQuestion(BaseModel):
    id: int
    chapter_id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    order_num: Optional[int]
    # correct_answer intentionally excluded

class SubmitRequest(BaseModel):
    user_id: str
    answer: str  # must be A | B | C | D

class SubmitResponse(BaseModel):
    correct: bool
    correct_answer: str
    explanation: str
    score: Optional[int] = None  # only on final (5th) question

# ── Progress models ───────────────────────────────────────────────────────────

class ChapterProgress(BaseModel):
    chapter_id: int
    title: str
    completed: bool
    score: Optional[int]
    attempts: int

class ProgressResponse(BaseModel):
    tier: str
    streak_days: int
    avg_score: float
    chapters_completed: int
    chapters: list[ChapterProgress]

class ProgressUpdateRequest(BaseModel):
    chapter_id: int
    completed: bool
    score: Optional[int] = None

# ── Auth models ───────────────────────────────────────────────────────────────

class AuthRegisterRequest(BaseModel):
    email: str
    password: str

class AuthLoginRequest(BaseModel):
    email: str
    password: str

class AuthRegisterResponse(BaseModel):
    user_id: str
    email: str
    tier: str

class AuthLoginResponse(BaseModel):
    access_token: str
    user_id: str
    tier: str

# ── Access models ─────────────────────────────────────────────────────────────

class AccessCheckResponse(BaseModel):
    allowed: bool
    required_tier: Optional[str] = None
    user_tier: Optional[str] = None

# ── Search models ─────────────────────────────────────────────────────────────

class SearchResult(BaseModel):
    id: int
    title: str
    excerpt: str
    tier: str

# ── Admin models ──────────────────────────────────────────────────────────────

class AdminUpgradeRequest(BaseModel):
    user_id: str
    tier: str  # 'free' | 'premium' | 'pro'

# ── Hybrid LLM models (Phase 5) ───────────────────────────────────────────────

class GenerateQuestionRequest(BaseModel):
    user_id: str
    chapter_id: int

class GenerateQuestionResponse(BaseModel):
    question: str

class AdaptivePathRequest(BaseModel):
    user_id: str

class AdaptivePathResponse(BaseModel):
    recommended_next_chapter_id: int
    reasoning: str
    weak_areas: list[str]
    estimated_study_time_minutes: int

class AssessRequest(BaseModel):
    user_id: str
    chapter_id: int
    question: str
    answer: str

class AssessResponse(BaseModel):
    score: int  # 0–100
    feedback: str
    strengths: list[str]
    areas_to_improve: list[str]

# ── Shared auth user context ──────────────────────────────────────────────────

class AuthUser(BaseModel):
    user_id: str
    tier: str
