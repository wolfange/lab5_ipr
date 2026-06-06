# Lab 5 – Kubernetes deployment of Django application

## 📌 Описание

В данной лабораторной работе выполняется контейнеризация и развертывание Django-приложения из лабораторной работы №4 с использованием Kubernetes.

Приложение представляет собой систему управления скидками и пользователями.

---

## ⚙️ Стек технологий

- Python 3.12
- Django
- Docker
- Kubernetes (Kind / Minikube)
- YAML manifests

---

## 📁 Структура проекта

```
lab5_ipr/
└── lab4ci/
    ├── Dockerfile
    ├── README.md
    ├── requirements.txt
    ├── pyproject.toml
    ├── pytest.ini
    ├── uv.lock
    │
    ├── docs/
    │   └── api.md
    │
    ├── k8s/
    │   ├── namespace.yaml
    │   ├── configmap.yaml
    │   ├── secret.yaml
    │   ├── deployment.yaml
    │   ├── service.yaml
    │   ├── ingress.yaml
    │   └── hpa.yaml
    │
    ├── src/
    │   ├── manage.py
    │   ├── data_backup.json
    │   │
    │   ├── Sales_Aggregator/
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   ├── wsgi.py
    │   │   └── asgi.py
    │   │
    │   ├── users/
    │   │   ├── models.py
    │   │   ├── views.py
    │   │   ├── forms.py
    │   │   ├── urls.py
    │   │   └── migrations/
    │   │
    │   └── discounts/
    │       ├── models.py
    │       ├── views.py
    │       ├── forms.py
    │       ├── urls.py
    │       ├── admin.py
    │       ├── migrations/
    │       └── templates/
    │
    └── tests/
        ├── test_users.py
        └── test_discounts.py
```

---

## 🚀 Развертывание

### 1. Сборка Docker образа

```bash
docker build -t sales-aggregator:latest .
```

### 2. Запуск Kubernetes кластера

Использовался kind/minikube.
```bash
kind create cluster
```

### 3. Применение манифестов
```bash
kubectl apply -f k8s/
```
### 4. Проверка ресурсов
```bash
kubectl get pods -n lab5
kubectl get svc -n lab5
kubectl get hpa -n lab5
```

## Реализованные компоненты
- Deployment с репликами
- Service (NodePort)
- ConfigMap для конфигурации Django
- Secret для чувствительных данных
- Ingress для доступа к приложению
- HPA для автоскейлинга
- Resource limits и requests
- Liveness и readiness probes

## Доступ к приложению
http://localhost:30080
