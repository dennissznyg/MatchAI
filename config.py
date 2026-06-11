from urllib.parse import quote_plus
from adapters.jobindex import JobIndexAdapter

# Minimum score (0-100) for at et job tages med i den daglige email
MIN_SCORE = 65

# Tilføj adaptere her efter hvert kilde du vil søge i.
# JobIndex: lav en søgning på jobindex.dk, klik "Modtag som RSS" og indsæt linket.
# JobIndex's RSS understøtter ikke geo-filtrering, så vi filtrerer client-side
# på områdenavnet JobIndex selv viser på opslaget.
STORKOEBENHAVN_NORDSJAELLAND = [
    "københavn", "frederiksberg", "gentofte", "gladsaxe", "lyngby", "rødovre",
    "hvidovre", "glostrup", "albertslund", "ballerup", "herlev", "brøndby",
    "vallensbæk", "ishøj", "tårnby", "dragør", "taastrup", "værløse", "farum",
    "furesø", "hillerød", "helsingør", "hørsholm", "fredensborg", "allerød",
    "birkerød", "holte", "egedal", "frederikssund", "gribskov", "halsnæs",
    "storkøbenhavn", "hovedstadsområdet", "hjemmearbejdsplads",
]

# Søgeord der hver giver et separat JobIndex-feed.
SEARCH_TERMS = [
    "IT/OT",
    "GxP",
    "Digital transformation",
    "Manufacturing Intelligence",
    "Programme Manager",
    "Program Manager",
    "Pharma",
    "Life Science",
    "MES",
    "IIoT",
    "Industry 4.0",
    "Solution Architect",
    "Tech Lead",
    "Implementation consultant",
    "Implementation partner",
    "Digital partner",
    "Transformation consultant",
    "Data partner",
    "Senior Project Manager",
    "GxP TechLead",
]

ADAPTERS = [
    JobIndexAdapter(
        feed_urls=[
            f"https://www.jobindex.dk/jobsoegning.rss?q={quote_plus(term)}"
            for term in SEARCH_TERMS
        ],
        allowed_areas=STORKOEBENHAVN_NORDSJAELLAND,
    ),
    # Eksempel på fremtidig adapter:
    # WorkdayAdapter(company_url="https://novonordisk.wd3.myworkdayjobs.com/..."),
]
