import logging
import traceback
from dataclasses import dataclass
from typing import Callable, List, TypeVar


T = TypeVar("T")
LOGGER_NAME = "task_manager"


def configure_logger() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("task_manager.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


@dataclass
class AlertService:
    logger: logging.Logger

    def notify(self, operation: str, level: int, message: str) -> None:
        print("!!! Ошибка !!!")
        self.logger.warning(
            "ALERT | operation=%s | level=%s | message=%s",
            operation,
            logging.getLevelName(level),
            message,
        )

        if level >= logging.CRITICAL:
            # External integrations (Sentry, Application Insights, email) can be added here.
            self.logger.critical(
                "ALERT_EXTERNAL | operation=%s | target=Sentry/ApplicationInsights/Email",
                operation,
            )


@dataclass
class ExceptionHandler:
    logger: logging.Logger
    alerts: AlertService

    def handle(self, operation: str, exc: Exception, level: int = logging.ERROR) -> None:
        self.logger.log(
            level,
            "EXCEPTION | operation=%s | message=%s | stack_trace=%s",
            operation,
            str(exc),
            traceback.format_exc().strip(),
        )
        self.alerts.notify(operation, level, str(exc))


class TaskManager:
    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or configure_logger()
        self.tasks: List[str] = []
        self.alerts = AlertService(self.logger)
        self.exceptions = ExceptionHandler(self.logger, self.alerts)
        self.logger.info("TaskManager initialized")

    def _execute(self, operation: str, action: Callable[[], T], fallback: T, level: int = logging.ERROR) -> T:
        try:
            return action()
        except Exception as exc:
            self.exceptions.handle(operation, exc, level=level)
            return fallback

    def add_task(self, task: str) -> bool:
        def action() -> bool:
            if task is None:
                raise ValueError("Task text cannot be None")
            if not task.strip():
                raise ValueError("Task text cannot be empty")
            self.tasks.append(task)
            self.logger.info("RESULT | operation=Add | status=SUCCESS | task='%s'", task)
            return True

        return self._execute("Add", action, fallback=False, level=logging.ERROR)

    def remove_task(self, task: str) -> bool:
        def action() -> bool:
            if task is None:
                raise ValueError("Task text cannot be None")
            self.tasks.remove(task)
            self.logger.info("RESULT | operation=Remove | status=SUCCESS | task='%s'", task)
            return True

        return self._execute("Remove", action, fallback=False, level=logging.ERROR)

    def list_tasks(self) -> List[str]:
        def action() -> List[str]:
            snapshot = list(self.tasks)
            self.logger.info("RESULT | operation=List | status=SUCCESS | total=%d", len(snapshot))
            return snapshot

        return self._execute("List", action, fallback=[], level=logging.ERROR)
