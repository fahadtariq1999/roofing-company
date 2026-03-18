from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List


class TenantBase(BaseModel):
    name: str
    slug: str
    industry: str = 'roofing'
    theme_color: str = '#0f766e'
    hero_title: str
    hero_subtitle: str
    welcome_message: str
    system_prompt: str
    service_area: str
    contact_email: str
    contact_phone: str
    modules: List[str] = []


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    theme_color: Optional[str] = None
    hero_title: Optional[str] = None
    hero_subtitle: Optional[str] = None
    welcome_message: Optional[str] = None
    system_prompt: Optional[str] = None
    service_area: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    modules: Optional[List[str]] = None


class TenantOut(TenantBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PublicSiteConfig(BaseModel):
    name: str
    slug: str
    theme_color: str
    hero_title: str
    hero_subtitle: str
    welcome_message: str
    service_area: str
    contact_email: str
    contact_phone: str
    modules: List[str]


class ChatRequest(BaseModel):
    slug: str
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str


class LeadCreate(BaseModel):
    slug: str
    name: str
    email: Optional[EmailStr] = None
    phone: str
    address: Optional[str] = None
    need_type: Optional[str] = None
    notes: Optional[str] = None


class LeadOut(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    phone: str
    address: Optional[str] = None
    need_type: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    slug: str
    customer_name: str
    email: Optional[EmailStr] = None
    phone: str
    address: Optional[str] = None
    requested_slot: str
    issue_type: Optional[str] = None


class BookingOut(BaseModel):
    id: int
    customer_name: str
    email: Optional[str] = None
    phone: str
    address: Optional[str] = None
    requested_slot: str
    issue_type: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    tenant_name: str
    total_leads: int
    total_bookings: int
    total_messages: int
    latest_leads: List[LeadOut]
    latest_bookings: List[BookingOut]
