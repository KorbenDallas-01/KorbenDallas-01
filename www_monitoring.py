import csv
import time
import logging
from pathlib import Path
from datetime import datetime

import requests


URLS_FILE = "urls.txt"
REPORT_DIR = "reports"
REPORT_FILE = "website_status.csv"

CHECK_INTERVAL = 60  # sekund
TIMEOUT = 5

# overrride
Path(REPORT_DIR).mkdir(exist_ok=True)

report_path = Path(REPORT_DIR) / REPORT_FILE

logging.basicConfig(
    filename="monitor.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def load_urls(file_path):
    urls = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                url = line.strip()

                if url and not url.startswith("#"):
                    urls.append(url)

    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        print(f"Error: file {file_path} not found.")

    return urls


def create_report_if_not_exists():
    if not report_path.exists():
        with open(report_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp",
                "url",
                "status",
                "status_code",
                "response_time_ms"
            ])


def check_website(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=TIMEOUT)
        response_time = round((time.time() - start_time) * 1000)

        if response.status_code == 200:
            status = "OK"
        else:
            status = "WARNING"

        return status, response.status_code, response_time

    except requests.exceptions.Timeout:
        return "TIMEOUT", "NO RESPONSE", 0

    except requests.exceptions.ConnectionError:
        return "DOWN", "NO RESPONSE", 0

    except requests.exceptions.RequestException:
        return "ERROR", "NO RESPONSE", 0


def save_result(url, status, status_code, response_time):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(report_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            timestamp,
            url,
            status,
            status_code,
            response_time
        ])


def main():
    create_report_if_not_exists()

    print("Website monitor started. Press CTRL+C to stop.")
    logging.info("Website monitor started.")

    while True:
        urls = load_urls(URLS_FILE)

        if not urls:
            print("No URLs found in urls.txt")
            logging.warning("No URLs found.")
            time.sleep(CHECK_INTERVAL)
            continue

        for url in urls:
            status, status_code, response_time = check_website(url)

            print(f"{url} | {status} | {status_code} | {response_time} ms")

            save_result(url, status, status_code, response_time)

            logging.info(
                f"{url} | {status} | {status_code} | {response_time} ms"
            )

        print("-" * 60)
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
