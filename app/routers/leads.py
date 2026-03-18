from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import LeadCreate, LeadOut
from app.services.tenant_service import get_tenant_by_slug, parse_modules

router = APIRouter(prefix='/leads', tags=['leads'])


@router.post('', response_model=LeadOut)
def create_lead(req: LeadCreate, db: Session = Depends(get_db)):
    tenant = get_tenant_by_slug(db, req.slug)
    if not tenant:
        raise HTTPException(status_code=404, detail='Tenant not found')
    if 'lead_form' not in parse_modules(tenant.modules):
        raise HTTPException(status_code=400, detail='Lead form module is disabled for this tenant')

    lead = models.Lead(
        tenant_id=tenant.id,
        name=req.name,
        email=req.email,
        phone=req.phone,
        address=req.address,
        need_type=req.need_type,
        notes=req.notes,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
