"""
books_scraper.py
----------------
Scrapes book data from https://books.toscrape.com and exports it to a CSV file.

Usage:
    python scraper.py                        # scrape all pages
    python scraper.py --pages 3              # scrape first 3 pages
    python scraper.py --output my_books.csv  # custom output filename
    python scraper.py --pages 5 --output top_books.csv
"""

import csv
import logging
import time
import argparse
from dataclasses import dataclass, fields
from typing import Optional

import requests
from bs4 import BeautifulSoup

# ── Logging setup ──────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────────────

BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"
REQUEST_DELAY = 0.5  # seconds between requests (be polite to the server)

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

# ── Data model ─────────────────────────────────────────────────────────────────

@dataclass
class Book:
    title: str
    price: float
    rating: int        # 1–5
    availability: str
    url: str

# ── Scraping logic ─────────────────────────────────────────────────────────────

def fetch_page(url: str) -> Optional[BeautifulSoup]:
    """Fetch a URL and return a BeautifulSoup object, or None on failure."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP error fetching %s: %s", url, e)
    except requests.exceptions.ConnectionError:
        logger.error("Connection error — check your internet connection.")
    except requests.exceptions.Timeout:
        logger.error("Request timed out for %s", url)
    return None


def parse_price(raw: str) -> float:
    """Convert price string like '£12.99' to float 12.99."""
    return float(raw.replace("£", "").replace("Â", "").strip())


def parse_books(soup: BeautifulSoup) -> list[Book]:
    """Extract all books from a catalogue page."""
    books: list[Book] = []

    for article in soup.select("article.product_pod"):
        try:
            title = article.h3.a["title"]
            price = parse_price(article.select_one("p.price_color").text)
            rating_word = article.p["class"][1]  # e.g. "Three"
            rating = RATING_MAP.get(rating_word, 0)
            availability = article.select_one("p.availability").text.strip()
            relative_url = article.h3.a["href"].replace("../", "")
            full_url = BASE_URL + relative_url

            books.append(Book(
                title=title,
                price=price,
                rating=rating,
                availability=availability,
                url=full_url,
            ))
        except (AttributeError, KeyError, ValueError) as e:
            logger.warning("Skipped a book due to parsing error: %s", e)

    return books


def get_next_page_url(soup: BeautifulSoup) -> Optional[str]:
    """Return the URL of the next page, or None if we're on the last page."""
    next_btn = soup.select_one("li.next > a")
    if next_btn:
        return BASE_URL + next_btn["href"]
    return None


def scrape(max_pages: Optional[int] = None) -> list[Book]:
    """
    Scrape books.toscrape.com and return a list of Book objects.

    Args:
        max_pages: Maximum number of pages to scrape. Scrapes all if None.

    Returns:
        List of scraped Book objects.
    """
    all_books: list[Book] = []
    url: Optional[str] = START_URL
    page_num = 0

    while url:
        if max_pages and page_num >= max_pages:
            logger.info("Reached page limit (%d). Stopping.", max_pages)
            break

        page_num += 1
        logger.info("Scraping page %d — %s", page_num, url)

        soup = fetch_page(url)
        if soup is None:
            logger.error("Failed to fetch page %d. Stopping.", page_num)
            break

        books = parse_books(soup)
        all_books.extend(books)
        logger.info("  Found %d books (total so far: %d)", len(books), len(all_books))

        url = get_next_page_url(soup)
        if url:
            time.sleep(REQUEST_DELAY)

    return all_books


# ── CSV export ─────────────────────────────────────────────────────────────────

def export_to_csv(books: list[Book], filepath: str) -> None:
    """
    Write a list of Book objects to a CSV file.

    Args:
        books:    List of Book objects to export.
        filepath: Destination file path.
    """
    if not books:
        logger.warning("No books to export.")
        return

    column_names = [f.name for f in fields(Book)]

    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writeheader()
        for book in books:
            writer.writerow({
                "title": book.title,
                "price": f"{book.price:.2f}",
                "rating": book.rating,
                "availability": book.availability,
                "url": book.url,
            })

    logger.info("Exported %d books to '%s'.", len(books), filepath)


# ── CLI entry point ────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape books.toscrape.com and export results to CSV."
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=None,
        metavar="N",
        help="Number of pages to scrape (default: all pages)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="books.csv",
        metavar="FILE",
        help="Output CSV filename (default: books.csv)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logger.info("Starting scraper — target: books.toscrape.com")
    if args.pages:
        logger.info("Page limit: %d", args.pages)

    books = scrape(max_pages=args.pages)

    if books:
        export_to_csv(books, args.output)
        logger.info("Done. %d books saved to '%s'.", len(books), args.output)
    else:
        logger.error("No books were scraped. Check the logs above for errors.")


if __name__ == "__main__":
    main()
