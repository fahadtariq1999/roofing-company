from sqlalchemy.orm import Session
from app import models
from typing import Optional, List

from typing import Optional, List

def parse_modules(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(',') if item.strip()]



def serialize_modules(modules: Optional[List[str]]) -> str:
    return ','.join(modules or [])


def get_tenant_by_slug(db: Session, slug: str):
    return db.query(models.Tenant).filter(models.Tenant.slug == slug).first()
