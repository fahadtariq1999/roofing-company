from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PublicSiteConfig
from app.services.tenant_service import get_tenant_by_slug, parse_modules

router = APIRouter(prefix='/public', tags=['public'])


@router.get('/site/{slug}', response_model=PublicSiteConfig)
def get_public_site(slug: str, db: Session = Depends(get_db)):
    tenant = get_tenant_by_slug(db, slug)
    if not tenant:
        raise HTTPException(status_code=404, detail='Tenant not found')
    return PublicSiteConfig(
        name=tenant.name,
        slug=tenant.slug,
        theme_color=tenant.theme_color,
        hero_title=tenant.hero_title,
        hero_subtitle=tenant.hero_subtitle,
        welcome_message=tenant.welcome_message,
        service_area=tenant.service_area,
        contact_email=tenant.contact_email,
        contact_phone=tenant.contact_phone,
        modules=parse_modules(tenant.modules),
    )
