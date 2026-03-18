from sqlalchemy.orm import Session
from app.models import Tenant


def seed_data(db: Session):
    if db.query(Tenant).count() > 0:
        return

    tenants = [
        Tenant(
            name='Lone Star Roofing',
            slug='lone-star-roofing',
            theme_color='#ea580c',
            hero_title='Texas roofing leads on autopilot',
            hero_subtitle='Book more inspections with AI chat, smart forms, and instant response.',
            welcome_message='Hi, I can help with storm damage, roof replacement, or booking a free inspection.',
            system_prompt='Be helpful, local, concise, and focused on turning visitors into inspection bookings.',
            service_area='Dallas, Fort Worth, Austin, Houston',
            contact_email='hello@lonestarroofing.com',
            contact_phone='+1 214 555 0101',
            modules='chatbot,lead_form,booking,faq,estimate'
        ),
        Tenant(
            name='Empire State Roofing',
            slug='empire-state-roofing',
            theme_color='#2563eb',
            hero_title='New York roofing websites that convert',
            hero_subtitle='Capture more storm damage and replacement leads across NYC and nearby cities.',
            welcome_message='Ask about repairs, replacements, leaks, or insurance support.',
            system_prompt='Promote free inspections and keep responses professional and conversion-focused.',
            service_area='New York City, Buffalo, Rochester, Yonkers',
            contact_email='hello@empirestateroofing.com',
            contact_phone='+1 646 555 0133',
            modules='chatbot,lead_form,booking,faq'
        )
    ]
    db.add_all(tenants)
    db.commit()
