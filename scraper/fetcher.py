"""
fetcher.py
----------
Handles the network call. Kept separate from parsing so that each piece
can be tested / reused independently (e.g. swapped out for a cached
version, a different HTTP client, or mock data in tests).
"""

import requests

DEFAULT_TIMEOUT = 10  # seconds


def fetch_page(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """
    Download the HTML content for a given URL.

    Raises:
        requests.exceptions.RequestException: on any network / HTTP error.
    """
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text
