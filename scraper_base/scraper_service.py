import logging
import time
from typing import Optional, Type
from requests.exceptions import ConnectionError

import requests

from scraper_base import utils
from scraper_base.data_models import (JobResult, JobStatus, RequestType,
                                      ScraperJob)
from scraper_base.page_type_base import PageTypeBase
from scraper_base.result_processor_base import ResultProcessorBase

logger = logging.getLogger(__name__)


class ScraperService:
    """The base application that does the actual scraping. For any scraper this will provide a basis."""

    num_retries: int = 3
    """Number of times to retry faulty  requests"""
    wait_time = 5
    """Amount of time to wait before retrying"""
    default_wait_time = 5
    """used to reassign the wait_time to default"""

    def __init__(self, result_processor: Optional[Type[ResultProcessorBase]] = None) -> None:
        self.job_queue: list[ScraperJob] = []
        self.result_processor = result_processor
        self._is_running = False
        self.visited_urls = set()

    def run(self) -> None:
        while self._is_running:
            # sort the jobs in job queue according to priority level
            self.job_queue.sort(key=lambda x: x.priority, reverse=True)
            current_job = self.retrieve_job()
            if current_job:
                current_page_type = utils.get_page_type(current_job)
                if current_page_type:  # a page type has been found matching the job.
                    job_result = self.execute_job(current_page_type)
                    self.process_job_result(job_result, current_page_type)
            else:
                # there is no job in the queue, we may assume the scraping is done.
                self.stop_process()

    def process_job_result(self, job_result: JobResult, page_type: PageTypeBase) -> None:
        """Processes a given PageTypeBase by executing the request to the URL and adds new jobs to the queue if any."""
        new_jobs = page_type.find_new_jobs(job_result) or []

        # filter out the job url that are already visited
        new_jobs = [job for job in new_jobs if job.url not in self.visited_urls]
        self.job_queue.extend(new_jobs)
        # update the set of visited URLs with the URLs of the new jobs
        self.visited_urls.update(job.url for job in new_jobs)
        if page_type.process_result() and self.result_processor:
            self.result_processor.process_result(job_result)
        job_result.scraper_job.job_status = JobStatus.DONE

    def start_process(self) -> None:
        """Starts the process."""
        self._is_running = True
        self.run()

    def retrieve_job(self) -> Optional[ScraperJob]:
        """Retrieve a job from the job queue, checks if the job has the right status."""
        try:
            job = self.job_queue.pop(0)
            if job.job_status == JobStatus.PENDING:
                return job
            else:
                return self.retrieve_job()  # retrieve a new job from the queue.
        except IndexError:
            return None

    def stop_process(self) -> None:
        logger.info('Shut down scraper.')
        self._is_running = False

    @staticmethod
    def execute_job(page_type: PageTypeBase) -> JobResult:
        """Makes the request to the URL of the job, with the obtained data, create and return a JobResult"""
        request = None
        job = page_type.job
        job.job_status = JobStatus.IN_PROGRESS  # Set correct status

        for _ in range(ScraperService.num_retries):
            # retry if ConnectionError
            try:
                for i in range(ScraperService.num_retries + 1):
                    # retry if Request is unsuccessful
                    if job.request_type == RequestType.GET:
                        request = requests.get(job.url)
                    elif job.request_type == RequestType.POST:
                        request = requests.post(job.url, job.request_data)
                    if request is not None and request.status_code == 200:
                        break
                    elif i == ScraperService.num_retries:  # last try failed
                        break
                    logger.info(f"Retrying {job.request_type} request to {job.url} ({i + 1}/{ScraperService.num_retries})")
                    time.sleep(ScraperService.wait_time)

                    # increase wait time between retries
                    ScraperService.wait_time += 5
            except ConnectionError as e:
                logger.error(f"Connection error while trying to access {job.url}: {e}")
                time.sleep(ScraperService.wait_time)
                ScraperService.wait_time += 5
            else:
                # connection successful
                break
        # return wait_time to default amount
        ScraperService.wait_time = ScraperService.default_wait_time
        return JobResult(
            scraper_job=page_type.job,
            result=request.content if request else None,
            status_code=request.status_code if request else None,
            scraped_on=int(time.time())  # set current epoch.
        )
