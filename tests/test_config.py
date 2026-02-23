from autodoist_scheduler.config import SchedulerConfig


def test_config_from_env_defaults(monkeypatch) -> None:
    monkeypatch.setenv("AUTODOIST_EVENTS_INTERNAL_TRIGGER_URL", "http://autodoist-events:8081/internal/trigger")
    cfg = SchedulerConfig.from_env()
    assert cfg.trigger_url.endswith("/internal/trigger")
    assert cfg.interval_seconds == 900
    assert cfg.source == "cron_fallback"
    assert cfg.deliver is True
    assert cfg.dry_run is False


def test_config_from_env_overrides(monkeypatch) -> None:
    monkeypatch.setenv("AUTODOIST_EVENTS_INTERNAL_TRIGGER_URL", "http://x/internal/trigger")
    monkeypatch.setenv("AUTODOIST_EVENTS_INTERNAL_TOKEN", "abc")
    monkeypatch.setenv("AUTODOIST_EVENTS_SCHED_INTERVAL_SECONDS", "60")
    monkeypatch.setenv("AUTODOIST_EVENTS_SCHED_SOURCE", "cron_fallback")
    monkeypatch.setenv("AUTODOIST_EVENTS_SCHED_DELIVER", "false")
    monkeypatch.setenv("AUTODOIST_EVENTS_SCHED_DRY_RUN", "true")
    cfg = SchedulerConfig.from_env()
    assert cfg.internal_token == "abc"
    assert cfg.interval_seconds == 60
    assert cfg.deliver is False
    assert cfg.dry_run is True
