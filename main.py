import logging

from task_manager import TaskManager


def main() -> None:
    manager = TaskManager()

    print("Добавление валидной задачи:", manager.add_task("Подготовить релиз"))
    print("Добавление пустой задачи:", manager.add_task("   "))
    print("Текущий список задач:", manager.list_tasks())
    print("Удаление существующей задачи:", manager.remove_task("Подготовить релиз"))
    print("Удаление несуществующей задачи:", manager.remove_task("Несуществующая"))

    # Пример серьезной ошибки: вызываем централизованный обработчик вручную.
    try:
        raise RuntimeError("Критический сбой канала уведомлений")
    except RuntimeError as exc:
        manager.exceptions.handle("Notification", exc, level=logging.CRITICAL)


if __name__ == "__main__":
    main()
