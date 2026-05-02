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
# TODO: Populate with actual news sources for each country
_COUNTRY_NEWS_SOURCES: dict[str, list[str]] = {
    "US": [
        "https://feeds.bloomberg.com/markets/news.rss",
        "https://feeds.reuters.com/reuters/businessNews",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://feeds.theguardian.com/theguardian/us-news/rss",
        "https://feeds2.bloomberg.com/enterprise/topics/technology.rss",
        "https://www.huffpost.com/page/feeds/topbar-news",
    ],
    "GB": [
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://feeds.theguardian.com/theguardian/uk/rss",
        "https://feeds.wired.com/wired/index",
        "https://feeds.reuters.com/reuters",
        "https://feeds.bloomberg.com/markets/news.rss",
    ],
    "FR": [
        "https://www.lemonde.fr/rss/une.xml",
        "https://www.bfmtv.com/rss/news/",
        "https://feeds.reuters.com/reuters/fr",
        "https://api.france24.com/en/feed/rss",
    ],
    "DE": [
        "https://www.spiegel.de/international/index.rss",
        "https://feeds.reuters.com/reuters/germanBusinessNews",
        "https://www.dw.com/rssfeeds/en/rss-en-all",
        "https://www.tagesschau.de/xml/rss2",
    ],
    "CA": [
        "https://feeds.bloomberg.com/markets/news.rss",
        "https://feeds.reuters.com/reuters/businessNews",
        "https://www.bbc.com/news/rss.xml",
    ],
    "AU": [
        "https://feeds.abc.net.au/abc/news/",
        "https://feeds.reuters.com/reuters/worldNews",
        "https://www.bbc.com/news/rss.xml",
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
        "https://www.nationthailand.com/news",
        "https://world.thaipbs.or.th/feed/",
        "https://thethaiger.com/feed/",
        "https://www.pattayamail.com/feed/",
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

