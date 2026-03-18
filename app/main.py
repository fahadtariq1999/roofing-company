from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
from app.routers import public, chat, leads, bookings, admin
from app.seed import seed_data

app = FastAPI(title='Roofing SaaS API', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    seed_data(db)

app.include_router(public.router, prefix='/api')
app.include_router(chat.router, prefix='/api')
app.include_router(leads.router, prefix='/api')
app.include_router(bookings.router, prefix='/api')
app.include_router(admin.router, prefix='/api')


@app.get('/')
def root():
    return {'message': 'Roofing SaaS API is running'}
