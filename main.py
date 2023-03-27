import argparse

from scraper_base.data_models import ScraperJob
from scraper_base.scraper_service import ScraperService
from webshop_scraper.result_processors import ResultProcessor

parser = argparse.ArgumentParser(description='Scrape a http source.')
parser.add_argument('initial_url', type=str, help='The initial url to start scraping from.')
args = parser.parse_args()

if __name__ == '__main__':
    """Adds initial job to the scraper queue and starts it."""
    import webshop_scraper  # noqa: F401 ; need to import the scraper module for the sake of PageType discovery.

    app = ScraperService(ResultProcessor)
    app.job_queue.append(
        ScraperJob(
            url=args.initial_url,
        )
    )
    app.start_process()
    # NOTE: There should be no need to change this file, if you do so, then please elaborate why.
