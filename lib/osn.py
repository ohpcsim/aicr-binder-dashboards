"""Small public artifact loading helpers."""

from __future__ import annotations

from io import StringIO
from typing import Any

import pandas as pd
import requests


def fetch_text(url: str, timeout: int = 30) -> str:
    """Fetch a public text artifact."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def read_csv_url(url: str, timeout: int = 30, **kwargs: Any) -> pd.DataFrame:
    """Read a CSV artifact from a public URL."""
    return pd.read_csv(StringIO(fetch_text(url, timeout=timeout)), **kwargs)


def read_json_url(url: str, timeout: int = 30) -> Any:
    """Read a JSON artifact from a public URL."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()


def artifact_label(url: str) -> str:
    """Return a compact display label for an artifact URL."""
    return url.rstrip("/").split("/")[-1]

