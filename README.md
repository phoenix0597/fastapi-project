### Проект "Реализации системы бронирования отелей (backend часть)"

#### 1. Реализованный функционал
Проект представляет собой систему для бронирования отелей. Основные функции включают:

- **Регистрация и аутентификация пользователей**: Пользователи могут регистрироваться и авторизовываться в системе, используя электронную почту и пароль. Аутентификация осуществляется с использованием JWT-токенов (JSON Web Tokens).
- **Просмотр доступных отелей**: Пользователи могут искать отели по критериям, таким как локация и даты проживания.
- **Бронирование комнат**: Система позволяет пользователям бронировать комнаты в отелях.
- **Управление бронированиями**: Пользователи могут просматривать, добавлять и удалять свои бронирования.
- **Отправка подтверждений по электронной почте**: После успешного бронирования пользователи получают подтверждение на электронную почту.
- **Мониторинг и логирование**: Проект интегрирован с системами мониторинга `Prometheus` и `Grafana` для отслеживания метрик, а также использует `Sentry` для отслеживания ошибок.
- **Админ-панель для управления данными в базе данных**: Проект включает админ-панель, реализованную с использованием пакета `sqladmin`, что позволяет администраторам управлять записями пользователей, бронирований, отелей и номеров в удобном интерфейсе.

### Интерфейсы доступа приложения:
- **API**: документация по эндпоинтам: http://<HOST_IP>:9000/docs 
- **Web интерфейс**: http://<HOST_IP>:9000/pages/hotels?location=%D0%90%D0%BB%D1%82%D0%B0%D0%B9&date_from=2025-08-29&date_to=2025-09-12
 
    В качестве примера взяты следующие параметры запроса для поиска отеля (локация: Алтай, дата заезда: 29.08.2025, дата выезда: 12.09.2025. Первоначальная загрузка страницы искусствено замедлена для демоннстраации кэширования (последующие загрузки происходят быстро, поскольку получают данные из закэшированного ответа на первый HTTP-запрос к эндпоинту, время жизни кэша - 20 секунд)
    
    Здесь же можно сымитировать нагрузку на сервер, нажимая на соответствующие кнопки (включая генерацию ошибки `ZeroDivisionError`) и, перейдя в `Grafana`, просмотреть графики мониторинга.
- **Grafana**: http://<HOST_IP>:3000
- **Админ-панель для управления данными в БД**: http://<HOST_IP>:9000/admin (тестовый доступ логин: user@example.com, пароль: string)


#### 2. Использованные технологии

- **Язык программирования**: Python 3.12
- **Фреймворк**: FastAPI для создания RESTful API.
- **Аутентификация с использованием JWT**: JWT-токены используются для аутентификации пользователей. При успешной авторизации пользователю выдается JWT-токен, который используется для доступа к защищенным ресурсам.
  - Модули: В аутентификационных маршрутах используется библиотека для работы с JWT, которая декодирует и валидирует токены. Секретный ключ и алгоритм кодирования задаются в конфигурации.
  - Примеры использования: В `app/main.py` и `app/config.py` указаны настройки `SECRET_KEY` и `ALGORITHM`, используемые для генерации и проверки JWT-токенов.
- **База данных**: PostgreSQL с использованием SQLAlchemy для ORM. Асинхронное взаимодействие с базой данных осуществляется через библиотеку `asyncpg`.
  - Модуль: `app/database.py`
  - Примеры использования: Создание асинхронного движка базы данных и сессий для взаимодействия с базой данных.
- **Асинхронное программирование**: Использование `async/await` для выполнения асинхронных операций.
- **Очереди задач**: Celery используется для фоновых задач, таких как отправка писем.
  - Модуль: `docker-scripts/celery.sh`
- **Кэширование**: Redis используется в качестве кэша для FastAPI и брокера сообщений для Celery.
  - Модуль: `app/main.py`, инициализация FastAPICache с использованием RedisBackend.
- **Тестирование**: Используется `pytest` для написания и запуска тестов. Присутствуют как unit-тесты, так и интеграционные тесты.
  - Файлы: `app/tests/*`
- **Контейнеризация**: Docker используется для контейнеризации приложения и его зависимостей. Docker Compose управляет контейнерами для базы данных, Redis, Celery и других компонентов.
  - Файл: `docker-compose.yml`
- **Мониторинг и логирование**: Prometheus и Grafana используются для мониторинга метрик, таких как время ответа и использование памяти. Sentry используется для логирования ошибок.
  - Файл конфигурации: `prometheus.yml`
  - Примеры: `app/prometheus/router.py` предоставляет эндпоинты для тестирования метрик.
- **Статический анализ кода и автоматическое его форматирование**: Использование `flake8` и `Pyright` для статического анализа; `black`, `isort` и `autoflake` для автоматического форматирования кода.
  - Файлы конфигурации: `pyproject.toml` и `.flake8`


#### 3. Примененные паттерны проектирования ПО

- **DAO (Data Access Object)**: Паттерн DAO используется для абстракции доступа к данным, что позволяет изолировать бизнес-логику от прямых взаимодействий с базой данных. Классы, такие как `UsersDAO` и `BookingDAO`, отвечают за взаимодействие с соответствующими таблицами.
  - Пример: `app/bookings/dao.py` содержит класс `BookingDAO`, который инкапсулирует логику работы с таблицей бронирований.
- **Singleton**: Паттерн Singleton применяется в конфигурации приложения, чтобы гарантировать, что экземпляр класса настроек существует в единственном экземпляре.
  - Пример: `app/config.py` создает синглтон `Settings` для хранения конфигурационных параметров приложения.
- **Фабрика**: Паттерн Фабрика используется для создания объектов, таких как сессии базы данных.
  - Пример: В `app/database.py` используется фабрика `sessionmaker` для создания экземпляров сессий.
- **Middleware**: Паттерн Middleware используется для обработки запросов и ответов, добавляя дополнительную функциональность, такую как логирование и обработка CORS.
  - Пример: В `app/main.py` используется middleware для добавления заголовка времени выполнения запроса и обработки CORS.

#### 4. Соблюденные принципы ООП

- **Инкапсуляция**: Реализована через классы, инкапсулирующие данные и методы, работающие с ними. Примеры включают классы `BookingDAO`, `UsersDAO`, которые управляют доступом к данным.
- **Наследование**: Используется для создания базовых классов, которые затем расширяются более специфичными классами. Например, классы исключений в `app/exceptions.py` наследуются от базового класса `BookingException`.
- **Полиморфизм**: Полиморфизм реализован через использование базовых классов и интерфейсов. Это позволяет функциям работать с различными типами данных, поддерживая единый интерфейс.
- **Абстракция**: Применяется для создания абстракций над базой данных и другими сложными подсистемами. Это помогает изолировать детали реализации и предоставить простой API для использования другими частями системы.
