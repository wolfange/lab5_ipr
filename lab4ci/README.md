# Лабораторная работа №4: Непрерывная интеграция и доставка (CI/CD) в GitLab

## Sales Aggregator - CI/CD Pipeline

Веб-сервис для поиска, публикации и оценки студенческих скидок с настроенным CI/CD пайплайном в GitLab.

---

## 📋 Описание проекта

**Sales Aggregator** - это Django приложение, которое позволяет студентам:
- Публиковать информацию о скидках (кафе, магазины и т.д.)
- Оценивать чужие предложения (лайки/дизлайки)
- Сохранять понравившиеся посты в избранное
- Фильтровать посты по категориям
- Сортировать по рейтингу или дате

---

## 🏗️ Архитектура CI/CD Pipeline

### Этапы пайплайна:

```
┌──────────┐
│   Test   │  ← Unit-тесты с покрытием кода
└────┬─────┘
     │
┌────▼─────┐
│  Build   │  ← Сборка Docker-образа
└────┬─────┘
     │
┌────▼─────┐
│ Publish  │  ← Публикация в GitLab Container Registry
└──────────┘
```

### Этапы выполнения:

1. **Test** - Запуск unit-тестов с генерацией отчетов о покрытии кода
2. **Build** - Сборка Docker-образа приложения
3. **Test Image** - Проверка работоспособности собранного образа
4. **Publish** - Публикация образа в GitLab Container Registry (только для main/master веток)

---

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.12+
- Docker 20.10+
- GitLab аккаунт на [gitlab.mai.ru](https://gitlab.mai.ru)

### Локальная разработка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://gitlab.mai.ru/idt-lw/m8o-101bv-25/personal/IZKhammatov/lab4ci.git
   cd lab4ci
   ```

2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # или
   venv\Scripts\activate  # Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте переменные окружения:**
   Создайте файл `.env` в корне проекта:
   ```env
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=1
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   DB_NAME=sales_aggregator_db
   DB_USER=sales_user
   DB_PASSWORD=qwerty123
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Примените миграции:**
   ```bash
   cd src
   python manage.py migrate
   ```

6. **Запустите сервер разработки:**
   ```bash
   python manage.py runserver
   ```

7. **Откройте в браузере:**
   - Приложение: http://localhost:8000
   - Админ-панель: http://localhost:8000/admin

---

## 🧪 Тестирование

### Запуск тестов локально

```bash
# Запуск всех тестов
pytest

# Запуск с покрытием кода
pytest --cov=src --cov-report=html

# Запуск конкретного теста
pytest tests/test_users.py::CustomUserModelTest
```

### Структура тестов

- `tests/test_users.py` - Тесты для пользователей
- `tests/test_discounts.py` - Тесты для скидок и постов

### Покрытие кода

После запуска тестов с покрытием, отчет будет доступен в `htmlcov/index.html`

---

## 🐳 Docker

### Сборка образа локально

```bash
docker build -t sales-aggregator:latest .
```

### Запуск контейнера

```bash
docker run -p 8000:8000 sales-aggregator:latest
```

---

## 🔄 CI/CD Pipeline

### Конфигурация пайплайна

Пайплайн настроен в файле `.gitlab-ci.yml` и включает следующие этапы:

#### 1. Test Stage
- Запуск unit-тестов
- Генерация отчетов JUnit XML
- Расчет покрытия кода (coverage)
- Сохранение HTML отчета о покрытии

#### 2. Build Stage
- Сборка Docker-образа
- Тегирование образа по ветке и latest
- Проверка работоспособности образа

#### 3. Publish Stage
- Публикация образа в GitLab Container Registry
- Доступно только для веток `main` и `master`

### Переменные окружения

GitLab автоматически предоставляет следующие переменные:
- `CI_REGISTRY` - адрес Container Registry
- `CI_REGISTRY_IMAGE` - путь к образу проекта
- `CI_REGISTRY_USER` - имя пользователя для registry
- `CI_REGISTRY_PASSWORD` - пароль для registry
- `CI_COMMIT_REF_SLUG` - имя ветки (sanitized)

### Просмотр результатов

1. Перейдите в **CI/CD → Pipelines** в GitLab
2. Выберите нужный пайплайн
3. Просмотрите результаты каждого этапа
4. Скачайте артефакты (отчеты о покрытии, логи)

### Использование опубликованного образа

После успешной публикации образ будет доступен по адресу:
```
$CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG
```

Например:
```bash
docker pull registry.gitlab.mai.ru/group/project:main
```

---

## 📁 Структура проекта

```
lab4ci/
├── README.md               # Документация
├── .gitignore              # Игнорируемые файлы
├── .gitlab-ci.yml          # Конфигурация CI/CD пайплайна
├── Dockerfile              # Multi-stage Dockerfile
├── requirements.txt        # Зависимости Python
├── pytest.ini              # Конфигурация pytest
├── src/                    # Основной код приложения
│   ├── manage.py
│   ├── Sales_Aggregator/   # Django проект
│   │   ├── settings.py
│   │   └── ...
│   ├── users/              # Приложение пользователей
│   │   └── ...
│   └── discounts/          # Приложение скидок
│       └── ...
├── tests/                  # Unit-тесты
│   ├── test_users.py
│   └── test_discounts.py
└── docs/                   # Документация
    └── api.md
```

---
