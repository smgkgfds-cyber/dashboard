# Kubernetes

## Назначение

Kubernetes используется для оркестрации контейнеризированного приложения Corporate
Data Platform.

## Текущая конфигурация

- Deployment: corporate-data-deployment
- Используемый образ: corporate-data-app:2.0
- Количество экземпляров приложения: 3
- Порт приложения: 8000

## Подключение к базе данных

На данном этапе PostgreSQL продолжает работать как Docker Compose-сервис.
Kubernetes-приложение подключается к PostgreSQL через:

```
DB_HOST=host.docker.internal
DB_PORT=5432
```

Порт PostgreSQL 5432 опубликован в compose.yaml.

## Основные команды

Проверка кластера:

```
kubectl get nodes
```

Просмотр Pod:

```
kubectl get pods
```

Применение конфигурации:

```
kubectl apply -f kubernetes/deployment.yaml
```

Просмотр Deployment:

```
kubectl get deployments
```

Масштабирование:

```
kubectl scale deployment corporate-data-deployment --replicas=3
```

Просмотр журналов:

```
kubec
```
