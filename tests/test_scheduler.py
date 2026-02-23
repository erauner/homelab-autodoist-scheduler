from types import SimpleNamespace

from autodoist_scheduler.config import SchedulerConfig
from autodoist_scheduler.scheduler import Scheduler


class _FakeResponse:
    def __init__(self, status_code: int, payload: dict) -> None:
        self.status_code = status_code
        self._payload = payload
        self.text = str(payload)

    def json(self) -> dict:
        return self._payload


def test_trigger_once_with_token() -> None:
    cfg = SchedulerConfig(
        trigger_url="http://autodoist-events:8081/internal/trigger",
        internal_token="secret",
        interval_seconds=60,
    )
    sched = Scheduler(cfg)
    captured = {}

    def _post(url, json, headers, timeout):  # type: ignore[no-untyped-def]
        captured["url"] = url
        captured["json"] = json
        captured["headers"] = headers
        captured["timeout"] = timeout
        return _FakeResponse(200, {"ok": True, "audit_id": "a1"})

    sched.session = SimpleNamespace(post=_post)  # type: ignore[assignment]
    ok, status, body = sched.trigger_once()
    assert ok is True
    assert status == 200
    assert body and body.get("audit_id") == "a1"
    assert captured["headers"]["Authorization"] == "Bearer secret"


def test_trigger_once_failure() -> None:
    cfg = SchedulerConfig(
        trigger_url="http://autodoist-events:8081/internal/trigger",
        interval_seconds=60,
    )
    sched = Scheduler(cfg)

    def _post(url, json, headers, timeout):  # type: ignore[no-untyped-def]
        return _FakeResponse(500, {"ok": False, "error": "boom"})

    sched.session = SimpleNamespace(post=_post)  # type: ignore[assignment]
    ok, status, body = sched.trigger_once()
    assert ok is False
    assert status == 500
    assert body and body.get("error") == "boom"
