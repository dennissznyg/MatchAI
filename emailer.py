import os
import resend
from models import JobPosting


def send_digest(scored_postings: list[tuple[JobPosting, dict]], to_email: str) -> None:
    """scored_postings: liste af (JobPosting, {"score": int, "reason": str}), sorteret faldende efter score."""
    resend.api_key = os.environ["RESEND_API_KEY"]
    from_email = os.environ.get("RESEND_FROM", "job-finder@resend.dev")

    if not scored_postings:
        html = "<p>Ingen nye relevante jobopslag i dag.</p>"
    else:
        rows = []
        for posting, result in scored_postings:
            rows.append(f"""
                <div style="margin-bottom:20px;padding:12px;border:1px solid #ddd;border-radius:8px;">
                    <div style="font-size:18px;font-weight:bold;">
                        <a href="{posting.url}">{posting.title}</a>
                    </div>
                    <div style="color:#555;">{posting.company} &middot; {posting.location}</div>
                    <div style="margin-top:8px;">
                        <span style="background:#eef;padding:2px 8px;border-radius:4px;font-weight:bold;">
                            Score: {result['score']}/100
                        </span>
                    </div>
                    <div style="margin-top:8px;color:#333;">{result['reason']}</div>
                </div>
            """)
        html = "<h2>Dagens jobmatch</h2>" + "".join(rows)

    resend.Emails.send({
        "from": from_email,
        "to": to_email,
        "subject": f"Job-finder: {len(scored_postings)} relevante jobopslag",
        "html": html,
    })
