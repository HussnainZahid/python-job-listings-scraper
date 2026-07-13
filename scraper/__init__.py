"""
scraper package
----------------
A small, focused package for scraping job listings from the
Fake Python Jobs site (https://realpython.github.io/fake-jobs/).

Public API:
    fetch_page(url)        -> raw HTML string
    parse_job_cards(html)  -> list[JobListing]
    JobListing             -> dataclass with title/company/location/url
    to_dataframe(jobs)     -> pandas.DataFrame
    save_to_csv(jobs, path)-> writes a CSV file to disk
"""

from .fetcher import fetch_page
from .parser import JobListing, parse_job_cards
from .exporter import to_dataframe, save_to_csv

__all__ = [
    "fetch_page",
    "parse_job_cards",
    "JobListing",
    "to_dataframe",
    "save_to_csv",
]
