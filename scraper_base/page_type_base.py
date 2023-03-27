from abc import ABC, abstractmethod

from scraper_base.data_models import JobResult, ScraperJob


class PageTypeBase(ABC):
    """A type of page to scrape."""

    def __init__(self, job: ScraperJob) -> None:
        self.job = job

    @abstractmethod
    def find_new_jobs(self, job_result: JobResult) -> list[ScraperJob]:
        """
        This method finds new urls that should not be processed by the scraper application.

        Args:
            job_result (JobResult): The result from a scraper request.

        Returns:
            List[ScraperJob]: A list of ScraperJob objects that should be added as separate jobs.
        """

    @staticmethod
    @abstractmethod
    def url_matcher(url: str) -> bool:
        """
        Tries to match the url to determine if the url is of this page type.

        Args:
            url (str): url of the job to be matched against some pattern.

        Returns:
            bool: True if the url matches, False otherwise.
        """

    @staticmethod
    @abstractmethod
    def process_result() -> bool:
        """
        Notifies the scraper service that for this page type we want to pass it to the .

        Returns:
            bool: True when result needs to be processed, false otherwise.
        """
