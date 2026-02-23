import logging
import sys

from .config import SchedulerConfig
from .scheduler import Scheduler, install_signal_handlers


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    try:
        cfg = SchedulerConfig.from_env()
    except Exception as exc:
        logging.getLogger(__name__).error("invalid_config error=%s", exc)
        return 2
    scheduler = Scheduler(cfg)
    install_signal_handlers(scheduler)
    return scheduler.run_forever()


if __name__ == "__main__":
    sys.exit(main())
