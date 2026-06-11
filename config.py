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

ADAPTERS = [
    JobIndexAdapter(
        feed_urls=[
            "https://www.jobindex.dk/jobsoegning.rss?q=IT%2FOT+projektleder",
            "https://www.jobindex.dk/jobsoegning.rss?q=Senior+projektleder+life+science",
            "https://www.jobindex.dk/jobsoegning.rss?q=Digital+transformation+pharma",
            "https://www.jobindex.dk/jobsoegning.rss?q=GxP+konsulent",
            "https://www.jobindex.dk/jobsoegning.rss?q=Program+manager+pharma",
        ],
        allowed_areas=STORKOEBENHAVN_NORDSJAELLAND,
    ),
    # Eksempel på fremtidig adapter:
    # WorkdayAdapter(company_url="https://novonordisk.wd3.myworkdayjobs.com/..."),
]
