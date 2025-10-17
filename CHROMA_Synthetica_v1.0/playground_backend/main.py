from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from playground_backend.generator import generate_prompt_session
from playground_backend import storage
from playground_backend.models import (
    GenerateRequest,
    GenerateResponse,
    HistoryResponse,
    LikeRequest,
    ReferenceResponse,
    PromptSession,
)

app = FastAPI(
    title="SeaDream Prompt Playground",
    description="Web playground backend for generating SeaDream prompts.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
async def generate_prompt(request: GenerateRequest) -> GenerateResponse:
    try:
        generated = generate_prompt_session(
            brief=request.brief,
            model_name=request.model,
            theme_key=request.theme,
        )
    except HTTPException:
        raise

    session_payload = {
        "brief": request.brief,
        "theme": generated["theme"],
        "model_name": generated["model_name"],
        "blueprint": generated["blueprint"],
        "prompts": generated["prompts"],
        "payload": generated["payload"],
        "checklist_questions": generated.get("checklist_questions", []),
        "notes": generated.get("notes", []),
        "tags": request.tags or [],
        "case_id": request.case_id,
    }

    stored = storage.add_session(session_payload)
    return GenerateResponse(session=PromptSession(**stored))


@app.get("/history", response_model=HistoryResponse)
async def get_history() -> HistoryResponse:
    entries = [PromptSession(**entry) for entry in storage.list_history()]
    return HistoryResponse(items=entries)


@app.post("/history/{session_id}/like", response_model=GenerateResponse)
async def like_session(session_id: str, request: LikeRequest) -> GenerateResponse:
    updated = storage.set_like(session_id, request.liked)
    return GenerateResponse(session=PromptSession(**updated))


@app.get("/references", response_model=ReferenceResponse)
async def get_references() -> ReferenceResponse:
    entries = [PromptSession(**entry) for entry in storage.list_references()]
    return ReferenceResponse(items=entries)

