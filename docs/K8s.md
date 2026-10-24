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

## Service

Для предоставления стабильной точки доступа к приложению создан Service:

```
corporate-data-service.
```

Service выбирает Pod по метке:

```
app=corporate-data-app
```

18
Service принимает запросы на порту 80 и передает их приложению на порт 8000.

## ConfigMap

Для хранения параметров конфигурации создан ConfigMap:

```
corporate-data-config
```

В ConfigMap находятся не конфиденциальные параметры подключения к PostgreSQL и
параметры среды приложения.

## Масштабирование

Приложение управляется Deployment:

```
corporate-data-deployment
```

Итоговое количество экземпляров приложения: 2

## CI/CD

GitHub Actions проверяет синтаксис Python и собирает Docker-образ.

При push в `main` образ публикуется в GHCR с тегами `latest` и Git SHA. При push релизного тега `v*` публикуется версия релиза и обновляется `latest`.

Kubernetes использует конкретный тег образа, например `2.2.0`. Это позволяет явно определить версию приложения, развёрнутую в кластере.

Автоматическое развёртывание из GitHub Actions не настроено: после публикации образа обновление Kubernetes выполняется отдельно.
