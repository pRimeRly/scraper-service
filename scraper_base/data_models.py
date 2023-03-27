from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from bs4 import BeautifulSoup


class RequestType(Enum):
    """Type of HTTP request, either GET or POST."""
    GET = 'GET'
    POST = 'POST'


class JobStatus(Enum):
    """Defines the possible status of a job."""
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'


@dataclass
class ScraperJob:
    """Data related to a job to be executed by the scraper application."""
    url: str
    """Url of the job. Used as unique identifier."""
    request_type: RequestType = RequestType.GET
    """Type of HTTP request to be done by the scraper to the url. GET or POST."""
    job_status: JobStatus = JobStatus.PENDING
    """Status of job"""
    request_data: Optional[dict[str, Any]] = None
    """Optional request data in case of request_type=POST."""
    priority: Optional[int] = 0
    """Specifies the priority level of a certain job based on its PageType"""


@dataclass
class JobResult:
    """Holds the result of a scraper job."""
    scraper_job: ScraperJob
    """The ScraperJob which belongs to this JobResult."""
    result: Optional[bytes]
    """Bytes representation of the HTML/JSON scraped."""
    scraped_on: int
    """The timestamp (Epochs) on which the data was scraped."""
    status_code: Optional[int]
    """The HTTP status code of the return of the job HTTP request."""

    def get_soup(self) -> Optional[BeautifulSoup]:
        """Creates a BeautifulSoup instance from the JobResult instance if the request was successful."""
        if self.status_code and 300 > self.status_code >= 200 and self.result is not None:
            return BeautifulSoup(self.result, 'html.parser')
        return None
