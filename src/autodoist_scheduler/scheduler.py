import logging
import signal
import time
from dataclasses import asdict
from threading import Event
from typing import Any

import requests

from .config import SchedulerConfig

LOG = logging.getLogger(__name__)


class Scheduler:
    def __init__(self, cfg: SchedulerConfig) -> None:
        self.cfg = cfg
        self.stop_event = Event()
        self.session = requests.Session()

    def stop(self) -> None:
        self.stop_event.set()

    def trigger_once(self) -> tuple[bool, int | None, dict[str, Any] | None]:
        payload = {
            "source": self.cfg.source,
            "deliver": self.cfg.deliver,
            "dry_run": self.cfg.dry_run,
        }
        headers = {"Content-Type": "application/json"}
        if self.cfg.internal_token:
            headers["Authorization"] = f"Bearer {self.cfg.internal_token}"
        try:
            resp = self.session.post(
                self.cfg.trigger_url,
                json=payload,
                headers=headers,
                timeout=self.cfg.timeout_seconds,
            )
            body: dict[str, Any] | None = None
            try:
                body = resp.json()
            except Exception:
                body = {"raw": resp.text[:500]}
            ok = 200 <= resp.status_code < 300 and bool((body or {}).get("ok", True))
            return ok, resp.status_code, body
        except Exception as exc:
            return False, None, {"error": str(exc)}

    def run_forever(self) -> int:
        LOG.info("scheduler_start config=%s", asdict(self.cfg))
        if self.cfg.initial_delay_seconds > 0:
            LOG.info("scheduler_initial_delay seconds=%s", self.cfg.initial_delay_seconds)
            if self.stop_event.wait(self.cfg.initial_delay_seconds):
                return 0

        while not self.stop_event.is_set():
            started = time.monotonic()
            ok, status_code, body = self.trigger_once()
            if ok:
                LOG.info(
                    "scheduler_trigger_ok status=%s response=%s",
                    status_code,
                    body,
                )
            else:
                LOG.warning(
                    "scheduler_trigger_failed status=%s response=%s",
                    status_code,
                    body,
                )

            elapsed = time.monotonic() - started
            sleep_for = max(0.0, float(self.cfg.interval_seconds) - elapsed)
            if self.stop_event.wait(sleep_for):
                break
        LOG.info("scheduler_stop")
        return 0


def install_signal_handlers(scheduler: Scheduler) -> None:
    def _handle(_: int, __: object) -> None:
        scheduler.stop()

    signal.signal(signal.SIGTERM, _handle)
    signal.signal(signal.SIGINT, _handle)
