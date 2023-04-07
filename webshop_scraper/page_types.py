from typing import List, Optional
from scraper_base.data_models import JobResult, ScraperJob, JobStatus, RequestType
from scraper_base.page_type_base import PageTypeBase


class HomePage(PageTypeBase):
    """Page type class for the homepage"""

    @staticmethod
    def url_matcher(url: str) -> bool:
        """Matches the given url with the homepage"""
        return url == "https://site4scraping.nl/"

    def find_new_jobs(self, job_result: JobResult) -> Optional[List[ScraperJob]]:
        """Extracts product urls from the home page"""
        soup = job_result.get_soup()
        if soup:
            # Extract all href attributes from the page's anchor tags
            hrefs = [a_tag.get("href") for a_tag in soup.find_all('a')]
            valid_urls = list(set([url for url in hrefs if url.startswith('https://site4scraping.nl/')
                                   and url != "https://site4scraping.nl/"]))

            # list of new scraper job objects
            new_jobs = []
            for url in valid_urls:
                new_jobs.append(
                    ScraperJob(
                        url=url,
                        request_type=RequestType.GET,
                        request_data=None,
                        job_status=JobStatus.PENDING,
                        priority=set_page_type_priority(url)
                    )
                )
            return new_jobs
        else:
            return None

    @staticmethod
    def process_result() -> bool:
        return False


class ShopPage(PageTypeBase):
    """Page type class for the shop page"""

    @staticmethod
    def url_matcher(url: str) -> bool:
        """Matches the given url with the shop page"""
        return url.startswith("https://site4scraping.nl/shop/")

    def find_new_jobs(self, job_result: JobResult) -> Optional[List[ScraperJob]]:
        """Extracts product urls from the shop page"""
        soup = job_result.get_soup()
        if soup:
            # Extract all href attributes from the page's anchor tags
            hrefs = [a_tag.get("href") for a_tag in soup.find_all('a')]
            valid_urls = list(set([url for url in hrefs if url.startswith('https://site4scraping.nl/') and url
                                   not in ["https://site4scraping.nl/shop/", "https://site4scraping.nl/"]]))

            new_jobs = []
            for url in valid_urls:
                new_jobs.append(
                    ScraperJob(
                        url=url,
                        request_type=RequestType.GET,
                        request_data=None,
                        job_status=JobStatus.PENDING,
                        priority=set_page_type_priority(url)
                    )
                )
            return new_jobs
        else: 
            return None

    @staticmethod
    def process_result() -> bool:
        return False


class ProductPage(PageTypeBase):
    """Page type class for the Product pages"""

    @staticmethod
    def url_matcher(url: str) -> bool:
        """Matches the given url with the product page"""
        return url.startswith("https://site4scraping.nl/product/")

    def find_new_jobs(self, job_result: JobResult) -> Optional[List[ScraperJob]]:
        """Extracts product urls from the product page"""
        soup = job_result.get_soup()
        if soup:
            # Extract all href attributes from the page's anchor tags
            hrefs = [a_tag.get("href") for a_tag in soup.find_all('a')]
            valid_urls = list(set([url for url in hrefs if url.startswith('https://site4scraping.nl/')
                                   and url != "https://site4scraping.nl/"]))

            new_jobs = []
            for url in valid_urls:
                new_jobs.append(
                    ScraperJob(
                        url=url,
                        request_type=RequestType.GET,
                        request_data=None,
                        job_status=JobStatus.PENDING,
                        priority=set_page_type_priority(url)
                    )
                )
            return new_jobs
        else: 
            return None

    @staticmethod
    def process_result() -> bool:
        return True


def set_page_type_priority(url):
    """returns priority value based on page type"""
    for page_type in PageTypeBase.__subclasses__():
        if page_type.url_matcher(url):
            if page_type is ProductPage:
                return 2
            elif page_type is ShopPage:
                return 1
    return 0
