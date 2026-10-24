# Управление версиями Corporate Data Platform

## 1. Текущая версия

- Версия приложения: `2.2.0`
- Git-тег: `v2.2.0`
- Docker-образ: `ghcr.io/smgkgfds-cyber/dashboard:2.2.0`
- Kubernetes Deployment: `corporate-data-deployment`
- Количество реплик: `2`

## 2. Автоматическая сборка Docker-образа

Для автоматизации сборки используется GitHub Actions.

При публикации Git-тега, соответствующего шаблону `v*`, workflow:
1. Получает исходный код из Git.
2. Извлекает номер версии из тега.
3. Выполняет сборку Docker-образа.
4. Публикует версионированный образ в GitHub Container Registry.
5. Обновляет тег `latest`.

## 3. Развёртывание в Kubernetes

Для приложения используется объект Deployment с двумя репликами.

Применяется стратегия Rolling Update:
- `maxUnavailable: 1` — допускается недоступность не более одного пода во время обновления.
- `maxSurge: 1` — допускается создание одного дополнительного пода во время обновления.

Применение конфигурации:

```powershell
kubectl apply -f kubernetes/deployment.yaml
kubectl rollout status deployment/corporate-data-deployment
```

## 4. Проверка состояния приложения

Проверка Deployment и подов:

```powershell
kubectl get deployment corporate-data-deployment -o wide
kubectl get pods
```

Просмотр истории развёртываний:

```powershell
kubectl rollout history deployment/corporate-data-deployment
```

Проверка приложения через локальный порт:

```powershell
kubectl port-forward service/corporate-data-service 8080:80
```

После запуска проброса приложение доступно по адресу `http://localhost:8080`.

## 5. Откат неудачного обновления

Если новая версия приложения не запускается, можно восстановить предыдущую ревизию:

```powershell
kubectl rollout undo deployment/corporate-data-deployment
kubectl rollout status deployment/corporate-data-deployment
```

После отката необходимо проверить используемый Docker-образ, состояние подов и работоспособность приложения.

## 6. Результаты работы

В рамках практической работы:
- Создан Git-тег `v2.2.0`.
- Настроен GitHub Actions для сборки и публикации Docker-образа.
- Выполнено обновление приложения в Kubernetes.
- Проверена стратегия Rolling Update.
- Проверена история ревизий Deployment.
- Выполнен тестовый откат после имитации неудачного обновления.
- Подготовлена документация по управлению версиями и восстановлению приложения.