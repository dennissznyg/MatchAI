import re
import feedparser
from models import JobPosting
from adapters.base import JobSourceAdapter

AREA_RE = re.compile(r'jix_robotjob--area">(.*?)<')


class JobIndexAdapter(JobSourceAdapter):
    """Henter jobopslag fra JobIndex's RSS-feeds for en eller flere søgninger.

    Hver feed_url er et RSS-link genereret fra en søgning på jobindex.dk
    (klik "Modtag som RSS" på søgeresultatsiden).

    JobIndex's RSS understøtter ikke geo-filtrering via URL-parametre, så hvis
    `allowed_areas` angives, filtreres opslag client-side på områdenavnet
    (f.eks. "København", "Lyngby") som JobIndex selv angiver i opslaget.
    """

    def __init__(self, feed_urls: list[str], allowed_areas: list[str] | None = None):
        self.feed_urls = feed_urls
        self.allowed_areas = [a.lower() for a in allowed_areas] if allowed_areas else None

    def fetch(self) -> list[JobPosting]:
        postings: list[JobPosting] = []
        for feed_url in self.feed_urls:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = entry.get("title", "").strip()
                company = ""
                if " - " in title:
                    title_part, company = title.rsplit(" - ", 1)
                else:
                    title_part = title

                summary = entry.get("summary", "")
                area_match = AREA_RE.search(summary)
                area = area_match.group(1).strip() if area_match else ""

                if self.allowed_areas is not None:
                    if not any(a in area.lower() for a in self.allowed_areas):
                        continue

                postings.append(
                    JobPosting(
                        source="jobindex",
                        title=title_part.strip(),
                        company=company.strip(),
                        location=area,
                        url=entry.get("link", ""),
                        description=summary,
                        posted_date=entry.get("published", ""),
                    )
                )
        return postings
