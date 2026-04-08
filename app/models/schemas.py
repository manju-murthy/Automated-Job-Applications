from datetime import datetime

from pydantic import BaseModel, Field


class ResumeDocument(BaseModel):
    filename: str
    raw_text: str


class CandidateProfile(BaseModel):
    summary: str
    skills: list[str] = Field(default_factory=list)
    titles: list[str] = Field(default_factory=list)
    locations: list[str] = Field(default_factory=list)
    years_experience_estimate: int = 0
    source_documents: list[str] = Field(default_factory=list)


class JobPosting(BaseModel):
    source: str
    title: str
    company: str
    location: str
    url: str
    published_at: datetime
    description_snippet: str
    matching_skills: list[str] = Field(default_factory=list)


class JobSearchResponse(BaseModel):
    profile: CandidateProfile
    searched_at: datetime
    jobs: list[JobPosting]
