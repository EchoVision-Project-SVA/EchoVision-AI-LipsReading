from app.api import router as api_router
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

app = FastAPI(title="Lipreading API")

app.include_router(api_router, prefix="/api")

app.mount("/static", StaticFiles(directory="output_audio"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
