from typing import Optional

from scraper_base.data_models import ScraperJob
from scraper_base.page_type_base import PageTypeBase


def get_page_type(job: ScraperJob) -> Optional[PageTypeBase]:
    """
    Go over all possible page types and match the job to one.

    If the job has an url, it loops over the page types and checks for a match.
    If a match is found, it returns the initialized page type object.
    Otherwise, it returns None.

    Args:
        job (Job): the job to be matched.

    Returns:
        PageTypeBase: An initialized page type object for the given Job.
    """
    for page_type in PageTypeBase.__subclasses__():
        if page_type.url_matcher(job.url):
            return page_type(job)  # type: ignore
    return None
