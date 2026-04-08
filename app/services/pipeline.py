from datetime import UTC, datetime

from app.models.schemas import JobSearchResponse, ResumeDocument
from app.services.job_sources import RemotiveJobSource
from app.services.profile_builder import ProfileBuilder


class JobDiscoveryPipeline:
    def __init__(self) -> None:
        self._profile_builder = ProfileBuilder()
        self._job_source = RemotiveJobSource()

    async def run(self, resumes: list[ResumeDocument]) -> JobSearchResponse:
        profile = self._profile_builder.build(resumes)
        jobs = await self._job_source.search_recent(profile)
        jobs.sort(key=lambda item: item.published_at, reverse=True)
        return JobSearchResponse(profile=profile, searched_at=datetime.now(UTC), jobs=jobs)
