from pathlib import Path
from typing import Any, Dict, List, Optional, OrderedDict, Union, Tuple

from flask import redirect, request
from inginious.client.client import Client
from inginious.frontend.course_factory import CourseFactory
from inginious.frontend.courses import Course
from inginious.frontend.tasks import Task
from inginious.frontend.pages.course_admin.submission import (
    SubmissionPage,
)  # the page we want to modify
from inginious.frontend.pages.course_admin.utils import INGIniousAdminPage
from inginious.frontend.pages.utils import INGIniousAuthPage
from inginious.frontend.plugin_manager import PluginManager
from inginious.frontend.template_helper import TemplateHelper
from pymongo.collection import ReturnDocument
from bson.errors import InvalidId
from werkzeug.exceptions import NotFound, Forbidden, BadRequest
from werkzeug.wrappers.response import Response
from werkzeug.datastructures import ImmutableMultiDict
from pydantic import ValidationError

from .config import PluginConfig, get_config
from .grades import CodingStyleGrades, get_grades
from .logger import get_logger
from ._types import Submission, GradesIn

PLUGIN_PATH = Path(__file__).parent.absolute()
TEMPLATES_PATH = PLUGIN_PATH / "templates"

# The key to store style grade data in the submission's "custom" dict
PLUGIN_KEY = "coding_style"  # use plugin name from config?


class CodingStyleGradesOverview(INGIniousAuthPage):
    def GET_AUTH(self) -> str:
        """Displays all coding style grades for a given course for a user."""
        return self.user_manager.session_realname()

    def fetch_submission(self, submissionid: str) -> dict:
        """Slimmed down version of SubmissionPage.fetch_submission.
        Only returns dict (submission), instead of Tuple[Course, Task, dict]"""

        try:
            submission = self.submission_manager.get_submission(submissionid, False)
            if not submission:
                raise NotFound(description=_("This submission doesn't exist."))
        except InvalidId as ex:
            self._logger.info("Invalid ObjectId : %s", submissionid)
            raise Forbidden(description=_("Invalid ObjectId."))
        return submission


class CodingStyleGrading(INGIniousAdminPage):
    """Class that implements methods that allow administrators
    to grade the coding style of a submission."""

    _logger = get_logger()

    def __init__(self, config: PluginConfig, *args, **kwargs) -> None:
        self.config = config
        super().__init__(*args, **kwargs)

    def fetch_submission(self, submissionid: str) -> Submission:
        """Slimmed down version of `SubmissionPage.fetch_submission`.
        Only returns Submission, instead of Tuple[Course, Task, Submission]"""

        try:
            submission = self.submission_manager.get_submission(submissionid, False)
            if not submission:
                raise NotFound(description=_("This submission doesn't exist."))
        except InvalidId as ex:
            self._logger.info("Invalid ObjectId : %s", submissionid)
            raise Forbidden(description=_("Invalid ObjectId."))
        return submission

    def get_best_submission(
        self, courseid: str, taskid: str, username: str
    ) -> list:  # list what?
        return list(
            self.database.user_tasks.find(
                {"username": username, "courseid": courseid, "taskid": taskid},
                {"submissionid": 1, "_id": 0},
            )
        )

    def get_submissions(
        self, courseid: str = "tutorial", taskid: str = "04_run_student"
    ) -> List[Submission]:
        """Retrieves all submissions for a given task."""

        # get the task we want to find submissions for
        task = self.course_factory.get_task(courseid, taskid)

        # get all submissions
        submissions = self.submission_manager.get_user_submissions(
            task
        )  # type: List[Submission]

        return submissions
