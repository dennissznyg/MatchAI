# MatchAI - AI job-finder

Henter jobopslag, scorer dem mod din profil via Claude, og sender en daglig email med de mest relevante.

## Opsætning

1. **Profil**: Udfyld [profile/cv.md](profile/cv.md) med dit CV / relevante uddrag fra ansøgninger.

2. **Jobkilder**: I [config.py](config.py), tilføj RSS-feed-URL'er fra JobIndex.
   - Gå til jobindex.dk, lav en søgning, klik "Modtag som RSS", kopiér linket ind i `ADAPTERS`.

3. **Lokal kørsel**:
   ```
   pip install -r requirements.txt
   cp .env.example .env   # udfyld værdier
   python main.py
   ```
   (kør evt. `pip install python-dotenv` og indsæt `from dotenv import load_dotenv; load_dotenv()` øverst i main.py for lokal .env-support)

4. **GitHub Actions (daglig kørsel)**:
   - Push dette repo til GitHub (privat anbefalet, da `profile/cv.md` indeholder personlige data).
   - Tilføj secrets under Settings → Secrets and variables → Actions:
     - `ANTHROPIC_API_KEY`
     - `RESEND_API_KEY`
     - `RESEND_FROM` (afsenderadresse, kræver verificeret domæne i Resend)
     - `DIGEST_TO_EMAIL` (din email)
   - Workflowet [daily.yml](.github/workflows/daily.yml) kører hver dag kl. 06:00 UTC, eller manuelt via "Run workflow".

## Arkitektur

- `models.py` - fælles `JobPosting`-model for alle jobkilder
- `adapters/` - én adapter pr. jobkilde (kun JobIndex via RSS lige nu). Tilføj nye ved at
  implementere `JobSourceAdapter.fetch()` og returnere en liste af `JobPosting`.
- `storage.py` - SQLite-database der husker hvilke jobs der allerede er set/scoret
- `scorer.py` - sender nye jobs + din profil til Claude og får score 0-100 + begrundelse
- `emailer.py` - sender den daglige digest via Resend
- `config.py` - liste af adaptere og minimumsscore for at blive inkluderet

## Fremtidige kilder

For LinkedIn eller virksomheders ATS-systemer (Workday, SuccessFactors m.fl.):
lav en ny fil i `adapters/`, implementér `fetch() -> list[JobPosting]`, og tilføj instansen
til `ADAPTERS` i `config.py`. Mange ATS-systemer har en skjult JSON-API bag jobsiden, som
kan genbruges på tværs af virksomheder med samme system.
