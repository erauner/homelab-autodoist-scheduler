import os
from dataclasses import dataclass


def parse_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class SchedulerConfig:
    trigger_url: str
    internal_token: str | None = None
    interval_seconds: int = 900
    source: str = "cron_fallback"
    deliver: bool = True
    dry_run: bool = False
    timeout_seconds: float = 10.0
    initial_delay_seconds: int = 5

    @classmethod
    def from_env(cls) -> "SchedulerConfig":
        trigger_url = os.getenv("AUTODOIST_EVENTS_INTERNAL_TRIGGER_URL", "").strip()
        if not trigger_url:
            raise ValueError("AUTODOIST_EVENTS_INTERNAL_TRIGGER_URL is required")
        return cls(
            trigger_url=trigger_url,
            internal_token=(os.getenv("AUTODOIST_EVENTS_INTERNAL_TOKEN") or "").strip() or None,
            interval_seconds=max(5, int(os.getenv("AUTODOIST_EVENTS_SCHED_INTERVAL_SECONDS", "900"))),
            source=(os.getenv("AUTODOIST_EVENTS_SCHED_SOURCE") or "cron_fallback").strip() or "cron_fallback",
            deliver=parse_bool(os.getenv("AUTODOIST_EVENTS_SCHED_DELIVER"), True),
            dry_run=parse_bool(os.getenv("AUTODOIST_EVENTS_SCHED_DRY_RUN"), False),
            timeout_seconds=float(os.getenv("AUTODOIST_EVENTS_SCHED_TIMEOUT_SECONDS", "10")),
            initial_delay_seconds=max(
                0, int(os.getenv("AUTODOIST_EVENTS_SCHED_INITIAL_DELAY_SECONDS", "5"))
            ),
        )
