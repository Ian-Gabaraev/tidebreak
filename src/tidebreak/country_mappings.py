"""
Country code to country name mapping and news sources.
"""

# ISO 3166-1 Alpha-2 country codes to country names
_COUNTRY_NAMES: dict[str, str] = {
    "AO": "Angola",
    "AR": "Argentina",
    "AT": "Austria",
    "AU": "Australia",
    "BE": "Belgium",
    "BF": "Burkina Faso",
    "BH": "Bahrain",
    "BJ": "Benin",
    "BR": "Brazil",
    "CA": "Canada",
    "CH": "Switzerland",
    "CI": "Côte d'Ivoire",
    "CL": "Chile",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DE": "Germany",
    "DK": "Denmark",
    "EC": "Ecuador",
    "EE": "Estonia",
    "ES": "Spain",
    "ET": "Ethiopia",
    "FI": "Finland",
    "FR": "France",
    "GB": "United Kingdom",
    "GR": "Greece",
    "GW": "Guinea-Bissau",
    "HK": "Hong Kong",
    "HR": "Croatia",
    "ID": "Indonesia",
    "IE": "Ireland",
    "IT": "Italy",
    "JO": "Jordan",
    "KE": "Kenya",
    "KH": "Cambodia",
    "KR": "South Korea",
    "KW": "Kuwait",
    "LA": "Laos",
    "LK": "Sri Lanka",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "LV": "Latvia",
    "ME": "Montenegro",
    "ML": "Mali",
    "MT": "Malta",
    "MU": "Mauritius",
    "MX": "Mexico",
    "MY": "Malaysia",
    "NA": "Namibia",
    "NE": "Niger",
    "NL": "Netherlands",
    "NO": "Norway",
    "NP": "Nepal",
    "OM": "Oman",
    "PA": "Panama",
    "PH": "Philippines",
    "PL": "Poland",
    "PT": "Portugal",
    "RS": "Serbia",
    "RW": "Rwanda",
    "SG": "Singapore",
    "SI": "Slovenia",
    "SK": "Slovakia",
    "SN": "Senegal",
    "SV": "El Salvador",
    "TG": "Togo",
    "TH": "Thailand",
    "TR": "Turkey",
    "US": "United States",
    "VE": "Venezuela",
    "VN": "Vietnam",
    "XK": "Kosovo",
    "ZA": "South Africa",
}

# Country to News Source URLs mapping
_COUNTRY_NEWS_SOURCES: dict[str, list[str]] = {
    # ── Americas ──────────────────────────────────────────────────────
    "US": [
        "https://feeds.bloomberg.com/markets/news.rss",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://feeds.theguardian.com/theguardian/us-news/rss",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=United+States+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "CA": [
        "https://feeds.bloomberg.com/markets/news.rss",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://news.google.com/rss/search?q=Canada+news&hl=en-CA&gl=CA&ceid=CA:en",
    ],
    "AR": [
        "https://buenosairesherald.com/feed/",
        "https://www.batimes.com.ar/feed",
        "https://en.mercopress.com/rss",
        "https://news.google.com/rss/search?q=Argentina+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "BR": [
        "https://riotimesonline.com/feed/",
        "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Brazil+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "CL": [
        "https://www.santiagotimes.cl/feed/",
        "https://en.mercopress.com/rss",
        "https://news.google.com/rss/search?q=Chile+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "EC": [
        "https://en.mercopress.com/rss",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Ecuador+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "MX": [
        "https://mexiconewsdaily.com/feed/",
        "https://www.eluniversal.com.mx/rss.xml",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Mexico+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "PA": [
        "https://www.newsroompanama.com/feed",
        "https://en.mercopress.com/rss",
        "https://news.google.com/rss/search?q=Panama+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "SV": [
        "https://elfaro.net/en/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=El+Salvador+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "VE": [
        "https://www.caracaschronicles.com/feed/",
        "https://en.mercopress.com/rss",
        "https://news.google.com/rss/search?q=Venezuela+news&hl=en-US&gl=US&ceid=US:en",
    ],
    # ── Europe ────────────────────────────────────────────────────────
    "GB": [
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://feeds.theguardian.com/theguardian/uk/rss",
        "https://feeds.wired.com/wired/index",
        "https://feeds.bloomberg.com/markets/news.rss",
        "https://news.google.com/rss/search?q=United+Kingdom+news&hl=en-GB&gl=GB&ceid=GB:en",
    ],
    "FR": [
        "https://www.lemonde.fr/rss/une.xml",
        "https://www.bfmtv.com/rss/news/",
        "https://api.france24.com/en/feed/rss",
        "https://news.google.com/rss/search?q=France+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "DE": [
        "https://www.spiegel.de/international/index.rss",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://www.tagesschau.de/xml/rss2",
        "https://news.google.com/rss/search?q=Germany+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "AT": [
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Austria+news&hl=en-US&gl=US&ceid=US:en",
        "http://feeds.bbci.co.uk/news/rss.xml",
    ],
    "BE": [
        "https://rss.dw.com/rdf/rss-en-all",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://news.google.com/rss/search?q=Belgium+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "CH": [
        "https://rss.dw.com/rdf/rss-en-all",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://news.google.com/rss/search?q=Switzerland+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "CY": [
        "https://cyprus-mail.com/feed/",
        "https://in-cyprus.philenews.com/feed/",
        "https://news.google.com/rss/search?q=Cyprus+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "CZ": [
        "https://english.radio.cz/rss",
        "https://www.praguemorning.cz/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Czech+Republic+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "DK": [
        "https://rss.dw.com/rdf/rss-en-all",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://news.google.com/rss/search?q=Denmark+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "EE": [
        "https://news.err.ee/rss",
        "https://www.baltictimes.com/rss/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Estonia+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "ES": [
        "https://english.elpais.com/rss/elpais/inenglish.xml",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Spain+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "FI": [
        "https://rss.dw.com/rdf/rss-en-all",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://news.google.com/rss/search?q=Finland+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "GR": [
        "https://greekreporter.com/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Greece+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "HR": [
        "https://www.total-croatia-news.com/feed",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Croatia+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "IE": [
        "https://www.irishtimes.com/cmlink/news-1.1319192",
        "https://www.rte.ie/news/rss/news-headlines.xml",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://news.google.com/rss/search?q=Ireland+news&hl=en-IE&gl=IE&ceid=IE:en",
    ],
    "IT": [
        "https://www.ansa.it/english/news/rss.xml",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Italy+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "LT": [
        "https://www.lrt.lt/en/rss",
        "https://www.baltictimes.com/rss/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Lithuania+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "LU": [
        "https://www.wort.lu/en/rss",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Luxembourg+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "LV": [
        "https://eng.lsm.lv/rss/",
        "https://www.baltictimes.com/rss/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Latvia+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "ME": [
        "https://balkaninsight.com/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Montenegro+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "MT": [
        "https://lovinmalta.com/feed/",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://news.google.com/rss/search?q=Malta+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "NL": [
        "https://nltimes.nl/feed",
        "https://www.dutchnews.nl/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Netherlands+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "NO": [
        "https://www.newsinenglish.no/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Norway+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "PL": [
        "https://notesfrompoland.com/feed/",
        "https://www.thefirstnews.com/rss",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Poland+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "PT": [
        "https://www.theportugalnews.com/rss",
        "https://www.portugalist.com/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Portugal+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "RS": [
        "https://balkaninsight.com/feed/",
        "https://www.b92.net/eng/rss/news.xml",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Serbia+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "SI": [
        "https://www.rtvslo.si/feeds/00.xml",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Slovenia+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "SK": [
        "https://spectator.sme.sk/rss",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Slovakia+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "TR": [
        "https://www.hurriyetdailynews.com/rss",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Turkey+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "XK": [
        "https://balkaninsight.com/feed/",
        "https://prishtinainsight.com/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Kosovo+news&hl=en-US&gl=US&ceid=US:en",
    ],
    # ── Middle East ───────────────────────────────────────────────────
    "BH": [
        "https://vob.org/en/?feed=rss2",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://news.google.com/rss/search?q=Bahrain+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "JO": [
        "https://www.jordantimes.com/feed",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://news.google.com/rss/search?q=Jordan+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "KW": [
        "https://www.arabtimesonline.com/feed/",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://news.google.com/rss/search?q=Kuwait+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "OM": [
        "https://timesofoman.com/feed",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://news.google.com/rss/search?q=Oman+news&hl=en-US&gl=US&ceid=US:en",
    ],
    # ── Africa ────────────────────────────────────────────────────────
    "ZA": [
        "https://feeds.news24.com/articles/news24/TopStories/rss",
        "https://www.thesouthafrican.com/feed/",
        "https://mg.co.za/feed/",
        "https://www.dailymaverick.co.za/rss",
        "https://www.sabcnews.com/sabcnews/feed/",
        "https://www.iol.co.za/rss",
        "https://citizen.co.za/feed/",
    ],
    "AO": [
        "https://www.aljazeera.com/where/angola/",
        "https://clubofmozambique.com/feed/",
        "https://news.google.com/rss/search?q=Angola+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "BF": [
        "https://www.africanews.com/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Burkina+Faso+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "BJ": [
        "https://www.africanews.com/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Benin+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "CI": [
        "https://www.africanews.com/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Ivory+Coast+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "ET": [
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Ethiopia+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "GW": [
        "https://www.africanews.com/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Guinea-Bissau+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "KE": [
        "https://www.the-star.co.ke/rss",
        "https://nation.africa/kenya/rss",
        "https://www.standardmedia.co.ke/rss/headlines.php",
        "https://news.google.com/rss/search?q=Kenya+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "ML": [
        "https://www.africanews.com/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Mali+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "MU": [
        "https://defimedia.info/feed",
        "https://www.africanews.com/feed/",
        "https://news.google.com/rss/search?q=Mauritius+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "NA": [
        "https://www.namibian.com.na/feed/",
        "https://www.namibiansun.com/rss/feed",
        "https://news.google.com/rss/search?q=Namibia+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "NE": [
        "https://www.africanews.com/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Niger+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "RW": [
        "https://www.newtimes.co.rw/rssFeed",
        "https://www.ktpress.rw/feed/",
        "https://news.google.com/rss/search?q=Rwanda+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "SN": [
        "https://www.africanews.com/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Senegal+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "TG": [
        "https://www.africanews.com/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Togo+news&hl=en-US&gl=US&ceid=US:en",
    ],
    # ── Asia & Pacific ────────────────────────────────────────────────
    "AU": [
        "https://www.abc.net.au/news/feed/51120/rss.xml",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://news.google.com/rss/search?q=Australia+news&hl=en-AU&gl=AU&ceid=AU:en",
    ],
    "HK": [
        "https://www.scmp.com/rss/91/feed",
        "https://hongkongfp.com/feed/",
        "https://www.thestandard.com.hk/newsfeed/latest/news",
        "https://news.google.com/rss/search?q=Hong+Kong+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "ID": [
        "https://en.antaranews.com/rss/news.xml",
        "https://coconuts.co/jakarta/feed/",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Indonesia+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "KH": [
        "https://www.phnompenhpost.com/rss",
        "https://www.khmertimeskh.com/feed/",
        "https://news.google.com/rss/search?q=Cambodia+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "KR": [
        "https://koreajoongangdaily.joins.com/xmlFile/rss_join.xml",
        "https://en.yna.co.kr/RSS/news.xml",
        "https://www.koreaherald.com/common/rss_xml.php",
        "https://news.google.com/rss/search?q=South+Korea+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "LA": [
        "https://rss.dw.com/rdf/rss-en-all",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://news.google.com/rss/search?q=Laos+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "LK": [
        "https://www.dailymirror.lk/RSS_Feeds/breaking-news",
        "https://island.lk/feed/",
        "https://www.newsfirst.lk/feed/",
        "https://news.google.com/rss/search?q=Sri+Lanka+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "MY": [
        "https://www.freemalaysiatoday.com/feed/",
        "https://www.malaymail.com/feed/rss/malaysia",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://news.google.com/rss/search?q=Malaysia+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "NP": [
        "https://kathmandupost.com/rss",
        "https://myrepublica.nagariknetwork.com/rss",
        "https://thehimalayantimes.com/feed/",
        "https://news.google.com/rss/search?q=Nepal+news&hl=en-US&gl=US&ceid=US:en",
    ],
    "PH": [
        "https://www.philstar.com/rss/headlines",
        "https://www.philstar.com/rss/nation",
        "https://www.philstar.com/rss/business",
        "https://www.rappler.com/feed",
    ],
    "SG": [
        "https://www.straitstimes.com/news/singapore/rss.xml",
        "https://www.channelnewsasia.com/rss",
        "https://www.todayonline.com/feed",
        "https://news.google.com/rss/search?q=Singapore+news&hl=en-SG&gl=SG&ceid=SG:en",
    ],
    "VN": [
        "https://vietnamnews.vn/",
        "https://en.baodanang.vn/",
        "https://e.vnexpress.net/",
        "https://news.tuoitre.vn/vietnam-news.htm",
        "https://en.vietnamplus.vn/",
    ],
    "TH": [
        "https://www.nationthailand.com/",
        "https://www.nationthailand.com/thailand",
        "https://world.thaipbs.or.th/feed/",
        "https://thethaiger.com/feed/",
        "https://khaosodenglish.com/feed/",
    ],
}


def get_country_name(country_code: str) -> str:
    """
    Get country name from country code.

    Args:
        country_code: ISO 3166-1 Alpha-2 country code

    Returns:
        Country name

    Raises:
        ValueError: If country code is not found
    """
    if country_code not in _COUNTRY_NAMES:
        raise ValueError(f"Unknown country code: {country_code}")
    return _COUNTRY_NAMES[country_code]


def get_news_sources(country_code: str) -> list[str]:
    """
    Get news sources for a country.

    Args:
        country_code: ISO 3166-1 Alpha-2 country code

    Returns:
        List of news source URLs for the country

    Raises:
        ValueError: If country code is not found
    """
    if country_code not in _COUNTRY_NAMES:
        raise ValueError(f"Unknown country code: {country_code}")

    # Return country-specific sources if available, otherwise return empty list
    return _COUNTRY_NEWS_SOURCES.get(country_code, [])


def is_valid_country_code(country_code: str) -> bool:
    """Check if a country code is valid."""
    return country_code in _COUNTRY_NAMES


def get_all_supported_countries() -> dict[str, str]:
    """Get all supported country codes and names."""
    return _COUNTRY_NAMES.copy()
