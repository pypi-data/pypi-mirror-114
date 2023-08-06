from typing import Callable

from mpyzeebe.job.job import Job

ExceptionHandler = Callable[[Exception, Job], None]
