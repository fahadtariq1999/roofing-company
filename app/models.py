from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Tenant(Base):
    __tablename__ = 'tenants'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    industry = Column(String(80), default='roofing')
    theme_color = Column(String(20), default='#0f766e')
    hero_title = Column(String(255), default='Get a free roofing inspection')
    hero_subtitle = Column(Text, default='AI-powered roofing website that captures more leads.')
    welcome_message = Column(Text, default='Hi, I can help with estimates, inspections, and storm damage questions.')
    system_prompt = Column(Text, default='You are a helpful roofing sales assistant.')
    service_area = Column(Text, default='Dallas, Houston, Austin, San Antonio')
    contact_email = Column(String(150), default='sales@example.com')
    contact_phone = Column(String(50), default='+1 555 000 0000')
    modules = Column(Text, default='chatbot,lead_form,booking,faq,estimate')
    created_at = Column(DateTime, default=datetime.utcnow)

    leads = relationship('Lead', back_populates='tenant', cascade='all, delete')
    bookings = relationship('Booking', back_populates='tenant', cascade='all, delete')
    messages = relationship('ChatLog', back_populates='tenant', cascade='all, delete')


class Lead(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    name = Column(String(120), nullable=False)
    email = Column(String(150), nullable=True)
    phone = Column(String(50), nullable=False)
    address = Column(String(255), nullable=True)
    need_type = Column(String(80), nullable=True)
    notes = Column(Text, nullable=True)
    source = Column(String(50), default='website')
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant = relationship('Tenant', back_populates='leads')


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    customer_name = Column(String(120), nullable=False)
    email = Column(String(150), nullable=True)
    phone = Column(String(50), nullable=False)
    address = Column(String(255), nullable=True)
    requested_slot = Column(String(100), nullable=False)
    issue_type = Column(String(80), nullable=True)
    status = Column(String(30), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant = relationship('Tenant', back_populates='bookings')


class ChatLog(Base):
    __tablename__ = 'chat_logs'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    session_id = Column(String(120), nullable=False)
    user_message = Column(Text, nullable=False)
    bot_reply = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant = relationship('Tenant', back_populates='messages')
