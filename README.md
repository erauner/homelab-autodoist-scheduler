# homelab-autodoist-scheduler

Small scheduler process that periodically triggers the internal fallback endpoint in `homelab-autodoist-events`.

## Purpose

- Replaces legacy K8s CronJob inline logic.
- Keeps policy/orchestration in `autodoist-events`.
- Acts as thin heartbeat trigger only.

## Environment variables

- `AUTODOIST_EVENTS_INTERNAL_TRIGGER_URL` (required)
- `AUTODOIST_EVENTS_INTERNAL_TOKEN` (optional)
- `AUTODOIST_EVENTS_SCHED_INTERVAL_SECONDS` (default: `900`)
- `AUTODOIST_EVENTS_SCHED_SOURCE` (default: `cron_fallback`)
- `AUTODOIST_EVENTS_SCHED_DELIVER` (default: `true`)
- `AUTODOIST_EVENTS_SCHED_DRY_RUN` (default: `false`)
- `AUTODOIST_EVENTS_SCHED_TIMEOUT_SECONDS` (default: `10`)
- `AUTODOIST_EVENTS_SCHED_INITIAL_DELAY_SECONDS` (default: `5`)

## Local run

```bash
uv sync --group dev
uv run autodoist-events-scheduler
```
