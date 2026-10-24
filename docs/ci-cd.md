
# CI/CD

## Назначение

GitHub Actions автоматизирует проверку Python-кода, сборку Docker-образа и публикацию образов в GitHub Container Registry (GHCR).

## Триггеры

Workflow запускается при следующих событиях:

- Push в ветки `main` и `feature-ci`.
- Pull request в `main`.
- Push Git-тега, начинающегося с `v`.
- Ручной запуск через GitHub Actions.

## Этапы

1. Checkout — получение исходного кода репозитория.
2. Python syntax check — проверка синтаксиса `app/app.py` командой `python -m py_compile app/app.py`.
3. Docker Buildx — подготовка сборщика Docker.
4. Docker build — сборка тестового образа для ветки `feature-ci` и pull request.
5. GHCR login — авторизация в GitHub Container Registry при публикации.
6. Publish — публикация образа при push в `main` или при создании релизного тега `v*`.

## Docker Registry

Реестр: GitHub Container Registry (GHCR).

Путь к образу:

`ghcr.io/smgkgfds-cyber/dashboard`

При push в `main` публикуются теги:

- `latest` — последний опубликованный образ из `main`.
- Git SHA — конкретная версия исходного кода, например `ghcr.io/smgkgfds-cyber/dashboard:<commit-sha>`.

При push релизного тега `v2.2.0` публикуются теги `2.2.0` и `latest`.

## Права доступа

Workflow использует `contents: read` для чтения репозитория и `packages: write` для публикации Docker-образов. Для авторизации применяется встроенный `GITHUB_TOKEN`.

## CI и CD

CI выполняет автоматические проверки и сборку при изменениях кода.

Публикация Docker-образа является автоматизированным этапом доставки артефакта. Автоматическое развёртывание в Kubernetes этим workflow не выполняется.
