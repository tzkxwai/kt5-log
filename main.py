from task_manager import TaskManager


def main() -> None:
    manager = TaskManager()
    manager.add_task("Купить молоко")
    manager.add_task("Подготовить отчет")
    manager.add_task("   ")
    manager.list_tasks()
    manager.remove_task("Купить молоко")
    manager.remove_task("Несуществующая задача")
    manager.list_tasks()


if __name__ == "__main__":
    main()
