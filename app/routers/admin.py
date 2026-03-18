from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import TenantCreate, TenantOut, TenantUpdate, DashboardStats
from app.services.module_registry import AVAILABLE_MODULES
from app.services.tenant_service import parse_modules, serialize_modules, get_tenant_by_slug

router = APIRouter(prefix='/admin', tags=['admin'])


@router.get('/modules')
def get_modules():
    return AVAILABLE_MODULES


@router.get('/tenants', response_model=list[TenantOut])
def list_tenants(db: Session = Depends(get_db)):
    tenants = db.query(models.Tenant).order_by(models.Tenant.created_at.desc()).all()
    response = []
    for tenant in tenants:
        item = TenantOut.model_validate(tenant)
        item.modules = parse_modules(tenant.modules)
        response.append(item)
    return response


@router.post('/tenants', response_model=TenantOut)
def create_tenant(payload: TenantCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Tenant).filter(models.Tenant.slug == payload.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail='Tenant slug already exists')

    tenant = models.Tenant(
        name=payload.name,
        slug=payload.slug,
        industry=payload.industry,
        theme_color=payload.theme_color,
        hero_title=payload.hero_title,
        hero_subtitle=payload.hero_subtitle,
        welcome_message=payload.welcome_message,
        system_prompt=payload.system_prompt,
        service_area=payload.service_area,
        contact_email=payload.contact_email,
        contact_phone=payload.contact_phone,
        modules=serialize_modules(payload.modules),
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    result = TenantOut.model_validate(tenant)
    result.modules = parse_modules(tenant.modules)
    return result


@router.put('/tenants/{tenant_id}', response_model=TenantOut)
def update_tenant(tenant_id: int, payload: TenantUpdate, db: Session = Depends(get_db)):
    tenant = db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail='Tenant not found')

    for field, value in payload.model_dump(exclude_unset=True).items():
        if field == 'modules':
            setattr(tenant, field, serialize_modules(value))
        else:
            setattr(tenant, field, value)

    db.commit()
    db.refresh(tenant)
    result = TenantOut.model_validate(tenant)
    result.modules = parse_modules(tenant.modules)
    return result


@router.get('/dashboard/{slug}', response_model=DashboardStats)
def dashboard(slug: str, db: Session = Depends(get_db)):
    tenant = get_tenant_by_slug(db, slug)
    if not tenant:
        raise HTTPException(status_code=404, detail='Tenant not found')

    latest_leads = db.query(models.Lead).filter(models.Lead.tenant_id == tenant.id).order_by(models.Lead.created_at.desc()).limit(5).all()
    latest_bookings = db.query(models.Booking).filter(models.Booking.tenant_id == tenant.id).order_by(models.Booking.created_at.desc()).limit(5).all()

    return DashboardStats(
        tenant_name=tenant.name,
        total_leads=db.query(models.Lead).filter(models.Lead.tenant_id == tenant.id).count(),
        total_bookings=db.query(models.Booking).filter(models.Booking.tenant_id == tenant.id).count(),
        total_messages=db.query(models.ChatLog).filter(models.ChatLog.tenant_id == tenant.id).count(),
        latest_leads=latest_leads,
        latest_bookings=latest_bookings,
    )
