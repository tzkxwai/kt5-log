import logging
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Generator, List


LOGGER_NAME = "task_manager"


def configure_logger() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("task_manager.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


@dataclass
class TraceState:
    operation: str
    start_time: float


@contextmanager
def trace_operation(logger: logging.Logger, operation: str) -> Generator[TraceState, None, None]:
    state = TraceState(operation=operation, start_time=time.perf_counter())
    logger.info("TRACE START | operation=%s", operation)
    try:
        yield state
    except Exception as exc:
        duration_ms = (time.perf_counter() - state.start_time) * 1000
        logger.error(
            "TRACE END | operation=%s | result=ERROR | duration_ms=%.2f | reason=%s",
            operation,
            duration_ms,
            exc,
        )
        raise
    else:
        duration_ms = (time.perf_counter() - state.start_time) * 1000
        logger.info(
            "TRACE END | operation=%s | result=SUCCESS | duration_ms=%.2f",
            operation,
            duration_ms,
        )


class TaskManager:
    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.tasks: List[str] = []
        self.logger = logger or configure_logger()
        self.logger.info("TaskManager initialized")

    def add_task(self, task: str) -> None:
        with trace_operation(self.logger, "Add"):
            if not task.strip():
                self.logger.warning(
                    "RESULT | operation=Add | status=WARNING | reason=Empty task text"
                )
                return

            self.tasks.append(task)
            self.logger.info(
                "RESULT | operation=Add | status=SUCCESS | task='%s' | total=%d",
                task,
                len(self.tasks),
            )

    def remove_task(self, task: str) -> None:
        with trace_operation(self.logger, "Remove"):
            if task in self.tasks:
                self.tasks.remove(task)
                self.logger.info(
                    "RESULT | operation=Remove | status=SUCCESS | task='%s' | total=%d",
                    task,
                    len(self.tasks),
                )
            else:
                self.logger.warning(
                    "RESULT | operation=Remove | status=WARNING | reason=Task not found | task='%s'",
                    task,
                )

    def list_tasks(self) -> List[str]:
        with trace_operation(self.logger, "List"):
            if not self.tasks:
                self.logger.warning("RESULT | operation=List | status=WARNING | reason=No tasks")
                return []

            self.logger.info(
                "RESULT | operation=List | status=SUCCESS | total=%d",
                len(self.tasks),
            )
            return list(self.tasks)
