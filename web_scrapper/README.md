# 📚 Books Scraper

A command-line web scraper that collects book data from [books.toscrape.com](https://books.toscrape.com) and exports it to a CSV file.

> `books.toscrape.com` is a sandbox site built specifically for scraping practice — no terms of service are violated.

---

## Features

- Scrapes all 1000 books across 50 pages (or a custom number of pages)
- Extracts: title, price, star rating, availability, and direct URL
- Exports clean, structured data to CSV
- Polite scraping — includes a delay between requests
- Full error handling and logging
- CLI interface with `--pages` and `--output` flags

---

## Installation

```bash
git clone https://github.com/your-username/books-scraper.git
cd books-scraper
pip install -r requirements.txt
```

---

## Usage

```bash
# Scrape all pages → books.csv
python scraper.py

# Scrape first 3 pages only
python scraper.py --pages 3

# Custom output filename
python scraper.py --output top_rated.csv

# Both options combined
python scraper.py --pages 5 --output sample.csv
```

---

## Output

The resulting CSV contains the following columns:

| Column         | Example                              |
|----------------|--------------------------------------|
| `title`        | A Light in the Attic                 |
| `price`        | 51.77                                |
| `rating`       | 3                                    |
| `availability` | In stock                             |
| `url`          | https://books.toscrape.com/...       |

---

## Project Structure

```
books-scraper/
├── scraper.py        # Main script
├── requirements.txt  # Dependencies
└── README.md
```

---

## Dependencies

- [requests](https://docs.python-requests.org/) — HTTP requests
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) — HTML parsing

---
