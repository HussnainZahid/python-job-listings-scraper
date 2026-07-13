"""
exporter.py
-----------
Converts a list of JobListing records into other formats: a pandas
DataFrame (for display / filtering in Streamlit) and a CSV file (for
download / persistence).
"""

import csv
from dataclasses import asdict

import pandas as pd

from .parser import JobListing

FIELDNAMES = ["title", "company", "location", "url"]


def to_dataframe(jobs: list[JobListing]) -> pd.DataFrame:
    """Convert JobListing records into a pandas DataFrame."""
    if not jobs:
        return pd.DataFrame(columns=FIELDNAMES)
    return pd.DataFrame([asdict(job) for job in jobs])


def save_to_csv(jobs: list[JobListing], filepath: str) -> None:
    """Write job listings to a CSV file at the given path."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for job in jobs:
            writer.writerow(asdict(job))
