import abc

from scraper_base.data_models import JobResult


class ResultProcessorBase(abc.ABC):
    """
    Base class for result processor that take in a dataclass and processes it in a way defined by the concrete class.
    """

    @staticmethod
    @abc.abstractmethod
    def process_result(obj: JobResult) -> None:
        """Given any object which is a dataclass, process it."""
        pass

    @staticmethod
    def save_results() -> None:
        """Given the processed data, save it."""
        pass
