from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from api.routes import recipe

app = FastAPI(
  title=settings.PROJECT_NAME,
  version=settings.PROJECT_VERSION,
  description="A culinary knowledge hub powered by knowledge graphs"
)

# Configure CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Include routers
app.include_router(
  recipe.router,
  prefix=f"{settings.API_V1_STR}/recipes",
  tags=["recipes"]
)

@app.get("/")
async def root():
  return {
    "message": "Welcome to TasteGraph API",
    "version": settings.PROJECT_VERSION
  }