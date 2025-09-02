from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import dialogue, save

app = FastAPI(title="Kontrapunkt MVP API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dialogue.router, prefix="/dialogue", tags=["dialogue"])
app.include_router(save.router, prefix="/save", tags=["save"])

@app.get("/")
def root():
    return {"status": "ok", "engine": "Psycho-Noir Kontrapunkt", "mvp": True}
