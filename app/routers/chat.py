from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import ChatRequest, ChatResponse
from app.services.tenant_service import get_tenant_by_slug, parse_modules
from app.services.prompt_builder import build_prompt
from app.services.gemini_service import generate_reply

router = APIRouter(prefix='/chat', tags=['chat'])


@router.post('', response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    tenant = get_tenant_by_slug(db, req.slug)
    if not tenant:
        raise HTTPException(status_code=404, detail='Tenant not found')
    if 'chatbot' not in parse_modules(tenant.modules):
        raise HTTPException(status_code=400, detail='Chatbot module is disabled for this tenant')

    prompt = build_prompt(tenant, req.message)
    reply = generate_reply(prompt)

    log = models.ChatLog(
        tenant_id=tenant.id,
        session_id=req.session_id,
        user_message=req.message,
        bot_reply=reply,
    )
    db.add(log)
    db.commit()

    return ChatResponse(reply=reply)
