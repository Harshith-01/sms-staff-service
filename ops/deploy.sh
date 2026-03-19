#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="${SERVICE_NAME:-staff-service}"
PROJECT_DIR="${PROJECT_DIR:-/opt/staff-service}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
DEPLOY_BRANCH="${DEPLOY_BRANCH:-main}"

cd "$PROJECT_DIR"

export IMAGE_TAG

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
	git fetch --all --prune
	git checkout "$DEPLOY_BRANCH"
	git pull --rebase origin "$DEPLOY_BRANCH"
fi

docker compose -f "$COMPOSE_FILE" pull || true
docker compose -f "$COMPOSE_FILE" up -d --remove-orphans

docker image prune -f

echo "${SERVICE_NAME} deployed"
