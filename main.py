import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import anthropic
from pypdf import PdfReader

from config import ADAPTERS, MIN_SCORE
from storage import init_db, filter_new, mark_seen
from scorer import score_jobs
from emailer import send_digest

PROFILE_DIR = Path(__file__).parent / "profile"


def load_profile() -> str:
    """Læser alle .md, .txt og .pdf filer i profile/ og samler dem til én tekst."""
    parts = []
    for path in sorted(PROFILE_DIR.iterdir()):
        if path.suffix.lower() in (".md", ".txt"):
            text = path.read_text(encoding="utf-8")
        elif path.suffix.lower() == ".pdf":
            reader = PdfReader(str(path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            continue

        if text.strip():
            parts.append(f"## {path.name}\n{text.strip()}")

    if not parts:
        raise FileNotFoundError(
            f"Ingen profil-filer fundet i {PROFILE_DIR}. Læg dit CV (pdf/md/txt) i denne mappe."
        )
    return "\n\n".join(parts)


def main() -> None:
    profile = load_profile()
    conn = init_db()

    all_postings = []
    seen_ids = set()
    for adapter in ADAPTERS:
        for posting in adapter.fetch():
            if posting.id not in seen_ids:
                seen_ids.add(posting.id)
                all_postings.append(posting)

    new_postings = filter_new(conn, all_postings)
    print(f"Hentede {len(all_postings)} unikke jobs, {len(new_postings)} er nye.")

    if not new_postings:
        send_digest([], os.environ["DIGEST_TO_EMAIL"])
        return

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    scores = score_jobs(client, profile, new_postings)

    scored = []
    for posting in new_postings:
        result = scores.get(posting.id, {"score": 0, "reason": "Ingen score returneret."})
        mark_seen(conn, posting, result["score"])
        if result["score"] >= MIN_SCORE:
            scored.append((posting, result))

    scored.sort(key=lambda x: x[1]["score"], reverse=True)
    send_digest(scored, os.environ["DIGEST_TO_EMAIL"])
    print(f"Sendte {len(scored)} relevante jobs i digest.")


if __name__ == "__main__":
    main()
