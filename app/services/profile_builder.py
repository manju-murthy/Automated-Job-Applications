import re

from app.models.schemas import CandidateProfile, ResumeDocument

COMMON_SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "node",
    "sql",
    "postgresql",
    "aws",
    "docker",
    "kubernetes",
    "machine learning",
    "data analysis",
    "fastapi",
    "django",
    "flask",
    "golang",
    "c++",
}

COMMON_TITLES = [
    "software engineer",
    "senior software engineer",
    "backend engineer",
    "frontend engineer",
    "full stack engineer",
    "data scientist",
    "product manager",
    "devops engineer",
]


class ProfileBuilder:
    def build(self, docs: list[ResumeDocument]) -> CandidateProfile:
        combined_original = "\n".join(doc.raw_text for doc in docs)
        combined_text = combined_original.lower()

        skills = self._extract_skills(combined_text)
        titles = self._extract_titles(combined_text)
        locations = self._extract_locations(combined_original)
        years_experience = self._estimate_years(combined_text)

        summary = (
            f"Candidate has {years_experience}+ years estimated experience with focus on "
            f"{', '.join(skills[:5]) or 'general software development'}."
        )

        return CandidateProfile(
            summary=summary,
            skills=skills,
            titles=titles,
            locations=locations,
            years_experience_estimate=years_experience,
            source_documents=[doc.filename for doc in docs],
        )

    @staticmethod
    def _extract_skills(text: str) -> list[str]:
        return sorted(skill for skill in COMMON_SKILLS if skill in text)

    @staticmethod
    def _extract_titles(text: str) -> list[str]:
        return sorted(title for title in COMMON_TITLES if title in text)

    @staticmethod
    def _extract_locations(text: str) -> list[str]:
        pattern = re.compile(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*,\s?[A-Z]{2})\b")
        found: list[str] = []
        seen: set[str] = set()
        for match in pattern.findall(text):
            if match not in seen:
                seen.add(match)
                found.append(match)
        return found[:5]

    @staticmethod
    def _estimate_years(text: str) -> int:
        year_matches = re.findall(r"(\d+)\+?\s+years", text)
        if not year_matches:
            return 2
        return max(int(y) for y in year_matches)
