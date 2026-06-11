import json
import anthropic
from models import JobPosting

MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = """Du er en karriererådgiver, der vurderer jobopslag op imod en kandidats CV.
For hvert jobopslag skal du give:
- "score": et tal 0-100 for hvor godt jobbet matcher kandidatens profil og erfaring
- "reason": en kort begrundelse (maks 2 sætninger, på dansk)

Vær kritisk og realistisk - giv kun høje scores (80+) til jobs der reelt matcher kandidatens
erfaringsniveau, kompetencer og præferencer. Svar KUN med gyldig JSON, intet andet."""


def score_jobs(client: anthropic.Anthropic, profile: str, postings: list[JobPosting]) -> dict[str, dict]:
    """Returnerer {job_id: {"score": int, "reason": str}} for hver posting."""
    if not postings:
        return {}

    jobs_payload = [
        {
            "id": p.id,
            "title": p.title,
            "company": p.company,
            "location": p.location,
            "description": p.description[:2000],
        }
        for p in postings
    ]

    user_prompt = f"""## Kandidatens profil (CV/ansøgninger)
{profile}

## Jobopslag der skal vurderes
{json.dumps(jobs_payload, ensure_ascii=False, indent=2)}

Returner et JSON-array med ét objekt per job: [{{"id": "...", "score": 0-100, "reason": "..."}}]"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    results = json.loads(text)
    return {item["id"]: {"score": item["score"], "reason": item["reason"]} for item in results}
