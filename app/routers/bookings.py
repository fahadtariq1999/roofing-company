from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import BookingCreate, BookingOut
from app.services.tenant_service import get_tenant_by_slug, parse_modules

router = APIRouter(prefix='/bookings', tags=['bookings'])


@router.post('', response_model=BookingOut)
def create_booking(req: BookingCreate, db: Session = Depends(get_db)):
    tenant = get_tenant_by_slug(db, req.slug)
    if not tenant:
        raise HTTPException(status_code=404, detail='Tenant not found')
    if 'booking' not in parse_modules(tenant.modules):
        raise HTTPException(status_code=400, detail='Booking module is disabled for this tenant')

    booking = models.Booking(
        tenant_id=tenant.id,
        customer_name=req.customer_name,
        email=req.email,
        phone=req.phone,
        address=req.address,
        requested_slot=req.requested_slot,
        issue_type=req.issue_type,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking
