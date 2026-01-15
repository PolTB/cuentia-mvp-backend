from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import StoryRequest, StoryResponse
from app.pipeline import generate_story_pipeline
from app.config import settings

app = FastAPI(title="Cuentia MVP Backend",
    description="AI-powered children's story generation API", version="0.1.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    return {"message": "Cuentia MVP Backend API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/v1/generate-story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    try:
        response = await generate_story_pipeline(request)
        if not response.success:
            raise HTTPException(status_code=500, detail=response.error)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
