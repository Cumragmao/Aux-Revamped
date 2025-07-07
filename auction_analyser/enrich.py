"""Item enrichment utilities."""
import logging
from typing import Iterable

import requests
from bs4 import BeautifulSoup

from .models import Auction, Item

logger = logging.getLogger(__name__)


def fetch_item_name(item_id: int) -> str | None:
    """Fetch item name from Turtle WoW database."""
    url = f"https://database.turtle-wow.org/?item={item_id}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("Failed to fetch %s: %s", url, exc)
        return None
    soup = BeautifulSoup(resp.text, "html.parser")
    if soup.title:
        return soup.title.text.split("-")[0].strip()
    return None


def enrich_items(session):
    """Populate the items table with metadata."""
    item_ids = [row[0] for row in session.query(Auction.item_id).distinct()]
    for item_id in item_ids:
        if session.query(Item).filter_by(item_id=item_id).first():
            continue
        name = fetch_item_name(item_id)
        if not name:
            continue
        item = Item(item_id=item_id, name=name)
        session.add(item)
    session.commit()
