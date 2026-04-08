from fastapi import FastAPI, File, HTTPException, UploadFile

from app.models.schemas import ResumeDocument
from app.services.pipeline import JobDiscoveryPipeline
from app.services.resume_parser import ResumeParser, UnsupportedResumeTypeError

app = FastAPI(title="Automated Job Applications API", version="0.1.0")

parser = ResumeParser()
pipeline = JobDiscoveryPipeline()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/phase1/search-jobs")
async def phase1_search_jobs(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="At least one resume file is required")

    docs: list[ResumeDocument] = []
    for file in files:
        content = await file.read()
        try:
            text = parser.parse_bytes(file.filename or "resume.txt", content)
        except UnsupportedResumeTypeError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        if not text.strip():
            raise HTTPException(status_code=400, detail=f"No text extracted from {file.filename}")
        docs.append(ResumeDocument(filename=file.filename or "resume.txt", raw_text=text))

    result = await pipeline.run(docs)
    return result.model_dump()
