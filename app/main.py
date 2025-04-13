from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import router as api_router

app = FastAPI(title="Lipreading API")

# Allow all CORS origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Mount static files
app.mount("/static", StaticFiles(directory="output_audio"), name="static")

# Include your API routes
app.include_router(api_router, prefix="/api")

# Run with: python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
