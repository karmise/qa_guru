🚀 Reqres Mock Service

Небольшой мок-сервис на FastAPI, имитирующий работу reqres.in, и тесты на pytest для проверки его работы.

⸻

📦 Установка и запуск

1️⃣ Установите зависимости:
pip install fastapi uvicorn requests pytest

2️⃣ Запустите мок-сервис:
python mock_service.py

Сервис будет доступен на: http://0.0.0.0:8000
🔹 Доступные эндпоинты
| Метод | URL                      | Описание                             |
|-------|--------------------------|--------------------------------------|
| GET   | /api/users?page={n}       | Получить список пользователей        |
| GET   | /api/users/{id}           | Получить данные одного пользователя  |
| POST  | /api/users                | Создать пользователя                 |

'''📂 Структура проекта

├─ reqres.py                   # Мок-сервис на FastAPI
├─ test_users.py               # Тесты на requests + pytest
├─ test_users_with_mock.py     # Тесты на requests + pytest (c мок сервисом)
└─ README.md'''