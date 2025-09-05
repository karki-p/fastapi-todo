from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import Base, engine
from routers import todos as todos_router

# Create tables on startup (SQLite)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo App")

# CORS (handy in dev if you later host frontend elsewhere)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# API routes
app.include_router(todos_router.router)

# Serve frontend (index.html) from /  (define after API so /api/* works)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
