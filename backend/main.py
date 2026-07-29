from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from graph import graph
from pydantic import BaseModel
from utils.pdf_generator import generate_pdf
import os

app = FastAPI(
    title="Research Assistant API",
    version="1.0.0",
    description="Multi-Agent Research Assistant using LangGraph"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return {
        "message": "Research Assistant API is running"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }

class QueryRequest(BaseModel):
    query: str

@app.post("/research")
async def research(request: QueryRequest):

    state = {
        "query": request.query,
        "sub_questions": [],
        "research_results": [],
        "critique": {},
        "feedback": "",
        "retries": 0,
        "final_report": ""
    }

    result = graph.invoke(state)
    pdf_path = generate_pdf(
    result["final_report"],
    "reports/report.pdf"
)


    return {
    "report": result["final_report"],
    "critique": result["critique"],
    "download_url": f"/download/{os.path.basename(pdf_path)}"
}  

@app.get("/download/{filename}")
async def download_report(filename: str):

    path = f"reports/{filename}"

    if not os.path.exists(path):
        return {"error": "File not found"}

    return FileResponse(
        path=path,
        media_type="application/pdf",
        filename=filename
    )