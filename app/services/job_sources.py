from datetime import UTC, datetime, timedelta

import httpx

from app.models.schemas import CandidateProfile, JobPosting


class RemotiveJobSource:
    """Lightweight public job source for Phase 1 discovery."""

    BASE_URL = "https://remotive.com/api/remote-jobs"

    async def search_recent(self, profile: CandidateProfile) -> list[JobPosting]:
        query = self._build_query(profile)
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(self.BASE_URL, params={"search": query})
            response.raise_for_status()
            data = response.json()

        jobs: list[JobPosting] = []
        cutoff = datetime.now(UTC) - timedelta(hours=24)
        for item in data.get("jobs", []):
            published_raw = item.get("publication_date")
            if not published_raw:
                continue
            published_at = datetime.fromisoformat(published_raw.replace("Z", "+00:00"))
            if published_at < cutoff:
                continue

            description = item.get("description", "")
            matching_skills = [s for s in profile.skills if s.lower() in description.lower()]
            jobs.append(
                JobPosting(
                    source="remotive",
                    title=item.get("title", ""),
                    company=item.get("company_name", ""),
                    location=item.get("candidate_required_location", "Remote"),
                    url=item.get("url", ""),
                    published_at=published_at,
                    description_snippet=description[:250],
                    matching_skills=matching_skills,
                )
            )
        return jobs

    @staticmethod
    def _build_query(profile: CandidateProfile) -> str:
        parts: list[str] = []
        if profile.titles:
            parts.append(profile.titles[0])
        if profile.skills:
            parts.extend(profile.skills[:3])
        return " ".join(parts) or "software engineer"
