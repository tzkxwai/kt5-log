# TaskManager с централизованной обработкой исключений

Проект реализует операции `Add`, `Remove`, `List` и единый механизм обработки ошибок:
- перехват исключений в одном месте (`TaskManager._execute`);
- логирование `message`, `stack_trace`, контекста операции и уровня;
- оповещение через консоль (`!!! Ошибка !!!`) и запись в лог;
- заглушка для внешней интеграции при критических ошибках (Sentry/Application Insights/email).

## Запуск

```bash
python main.py
```

## Файлы

- `task_manager.py` — TaskManager, ExceptionHandler, AlertService.
- `main.py` — демонстрация успешных и ошибочных кейсов.
- `task_manager.log` — журнал событий и исключений.
- `REPORT.md` — краткий отчет по результатам.
