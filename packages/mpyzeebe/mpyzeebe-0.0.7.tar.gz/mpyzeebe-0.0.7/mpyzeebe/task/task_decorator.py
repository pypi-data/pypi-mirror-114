from typing import Callable

from mpyzeebe.job.job import Job

TaskDecorator = Callable[[Job], Job]
