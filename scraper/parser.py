"""
parser.py
---------
Turns raw HTML from the Fake Python Jobs site into a list of JobListing
records. All BeautifulSoup / HTML-structure knowledge lives here, so if
the site markup ever changes, this is the only file that needs updating.
"""

from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class JobListing:
    title: str
    company: str
    location: str
    url: str


def _get_text_or_default(element, default: str = "N/A") -> str:
    """Safely pull stripped text from a BeautifulSoup element."""
    if element is None:
        return default
    text = element.get_text(strip=True)
    return text if text else default


def parse_job_cards(html: str) -> list[JobListing]:
    """
    Parse the page HTML and return a list of JobListing records.

    Missing fields degrade gracefully to placeholder values instead of
    raising, so one malformed card never breaks the whole scrape.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Each job posting lives inside a <div class="card-content"> block.
    cards = soup.find_all("div", class_="card-content")

    jobs: list[JobListing] = []
    for card in cards:
        title_el = card.find("h2", class_="title")
        company_el = card.find("h3", class_="subtitle")
        location_el = card.find("p", class_="location")

        title = _get_text_or_default(title_el, "Unknown Title")
        company = _get_text_or_default(company_el, "Unknown Company")
        location = _get_text_or_default(location_el, "Unknown Location")

        # The footer has two links ("Learn" and "Apply") — the
        # detail-page URL we want lives on the "Apply" link.
        url = "N/A"
        for link in card.find_all("a", class_="card-footer-item"):
            if link.get_text(strip=True).lower() == "apply":
                url = link.get("href", "N/A")
                break

        jobs.append(JobListing(title=title, company=company, location=location, url=url))

    return jobs
