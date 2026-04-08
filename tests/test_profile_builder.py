from app.models.schemas import ResumeDocument
from app.services.profile_builder import ProfileBuilder


def test_profile_builder_merges_multiple_resumes():
    docs = [
        ResumeDocument(
            filename="resume_v1.txt",
            raw_text="Senior Software Engineer with 8 years experience. Python, AWS, Docker.",
        ),
        ResumeDocument(
            filename="resume_v2.txt",
            raw_text="Built backend services with FastAPI and PostgreSQL.",
        ),
    ]

    profile = ProfileBuilder().build(docs)

    assert profile.years_experience_estimate == 8
    assert "python" in profile.skills
    assert "aws" in profile.skills
    assert "docker" in profile.skills
    assert "fastapi" in profile.skills
    assert "senior software engineer" in profile.titles
    assert profile.source_documents == ["resume_v1.txt", "resume_v2.txt"]
