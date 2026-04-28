# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Run locally (Streamlit serves on `http://localhost:8501`):

```bash
source .venv/bin/activate
streamlit run src/app.py
```

Run via Docker for parity with production image:

```bash
docker-compose up --build
```

Build/push the production image manually (normally done by CI):

```bash
docker build --pull -t fuzzy-learn:local .
```

There is no test suite, no linter config, and no formatter config in the repo. Don't invent commands for them.

## Architecture

Single-page Streamlit app (`src/app.py`) backed by a small fuzzy-logic library (`utils/fuzzy_logic.py`). The app is the only entrypoint; everything else exists to support running it locally, in Docker, or on ECS.

### Two parallel fuzzy implementations — important

The codebase contains **two distinct fuzzy implementations that don't share code**:

- `utils/fuzzy_logic.py` — uses `scikit-fuzzy` over numpy arrays (continuous universe of discourse). Exposes `FuzzySystem` (generic membership-function builder) and `HeightPersistenceSystem` (the height + persistence → group classifier rendered in the app).
- `src/app.py` defines a `ConjuntoFuzzy` class — a from-scratch, dict-based implementation (`{element: degree}`) for discrete fuzzy sets. Used by the "Conjuntos Fuzzy" tab for set operations (união, interseção, complemento, potência, etc.).

When changing fuzzy behavior, identify which layer the user means: the continuous skfuzzy pipeline, or the discrete `ConjuntoFuzzy` set-theory demo. They are not interchangeable.

`src/app.py` prepends the repo root to `sys.path` at import time (line 8) so it can `from utils.fuzzy_logic import ...` regardless of CWD. Don't "clean up" that block — it's load-bearing for both `streamlit run src/app.py` and the Docker `CMD`.

### Deploy pipeline (AWS ECS Fargate)

`.github/workflows/deploy-ecs.yml` runs on push to `master`. Flow: build → push to ECR (tags `:<sha>` and `:latest`) → render `infra/ecs/task-definition.json` (substituting `AWS_ACCOUNT_ID_PLACEHOLDER` / `AWS_REGION_PLACEHOLDER` via `sed`, then injecting the new image via `aws-actions/amazon-ecs-render-task-definition`) → `UpdateService` with `wait-for-service-stability: true`.

Required GitHub Secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_ACCOUNT_ID`. Validated by the first workflow step before any AWS call.

Concurrency group `deploy-ecs-${{ github.ref }}` with `cancel-in-progress: true` — pushing twice in a row cancels the older run.

### Region / naming drift to watch

The README (Portuguese) documents region `us-east-1` and container name `fuzzy-learn-app`, but the **actual deployed infrastructure** uses:

| Setting | Value |
|---|---|
| Region | `sa-east-1` |
| Container name | `fuzzy-learn` (must match `containerDefinitions[0].name` in `task-definition.json` and `CONTAINER_NAME` in the workflow `env`) |
| Cluster / Service | `fuzzy-learn-cluster` / `fuzzy-learn-service` |
| ALB / Target Group | `fuzzy-learn-alb` / `fuzzy-learn-tg` (port 8501, health path `/_stcore/health`) |
| Log group | `/ecs/fuzzy-learn` |

The container name must be identical in three places: workflow `env.CONTAINER_NAME`, `infra/ecs/task-definition.json`'s `containerDefinitions[0].name`, and the ECS service's load-balancer container binding. A mismatch here caused commit `c7764ef`.

### Health checks

Two health checks exist and both must stay aligned with the Streamlit port (8501) and path (`/_stcore/health`):

1. Container-level health check in `Dockerfile` and in `task-definition.json` (`python -c "urllib.request.urlopen(...)"` — chosen because the slim image has no `curl`).
2. ALB target-group health check (configured in AWS console, not in this repo).

If you change the Streamlit port, all three locations need updating plus `portMappings` and the target group.

### ECS service networking constraint

The ECS service's subnets must be a subset of the AZs the ALB covers. If a task lands in an AZ not registered with the ALB, target registration fails with `Target is in an Availability Zone that is not enabled for the load balancer`, and the service loops unhealthy → never reaches steady state → the GitHub Action hangs in `wait-for-service-stability` until timeout. Fix is on the AWS side (update service subnets or add the AZ to the ALB), not in this repo.
