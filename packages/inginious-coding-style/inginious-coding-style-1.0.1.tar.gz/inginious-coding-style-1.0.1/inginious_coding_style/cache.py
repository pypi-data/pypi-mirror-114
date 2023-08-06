from functools import cached_property
from typing import Any, Dict, List, Optional, OrderedDict as OrderedDictType
from collections import OrderedDict

from ._types import Submission


def get_cache_decorator() -> Any:  # TODO: type annotation
    # try to use Python 3.9's cache decorator
    # TODO: test on python3.9
    try:
        from functools import cache  # type: ignore
    except ImportError:
        from functools import lru_cache, partial

        cache = partial(lru_cache, None)  # fall back on lru_cache(None)
    return cache


cache = get_cache_decorator()


class BestSubmission:
    def __init__(self, submissions: List[Submission]) -> None:
        # self._submissions = submissions
        self.len = len(submissions)
        best = None
        for submission in submissions:
            if best is None or submission["grade"] > best["grade"]:
                best = submission
        self.best_submission = best


class BestSubmissionCache:
    """Simple class that caches the best user submissions."""

    MAX_CACHE = 500  # TODO: add way to modify this number

    def __init__(self) -> None:
        self._cache: OrderedDictType[str, BestSubmission] = OrderedDict()

    def get(
        self, userid: str, courseid: str, submissions: List[Submission]
    ) -> Optional[Submission]:
        """Retrieves the best submission for a specific course for a given user."""
        s = self._cache.get(f"{userid}{courseid}")
        if s is not None and s.len == len(submissions):
            return s.best_submission
        return (self.add(userid, courseid, submissions)).best_submission

    def add(
        self, userid: str, courseid: str, submissions: List[Submission]
    ) -> BestSubmission:
        """Adds (and overwrites existing) user submissions for a course to the cache."""
        if len(self._cache) >= self.MAX_CACHE:
            self._cache.popitem(False)  # pop FIFO
        s = BestSubmission(submissions)
        self._cache[f"{userid}{courseid}"] = s
        return s
