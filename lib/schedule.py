import schedule as sched
import time
import logging

logger = logging.getLogger(__name__)

def schedule_bot(bot, run_every):
    interval, unit = parse_interval(run_every)
    if unit == 'minutes':
        sched.every(interval).minutes.do(run_bot, bot)
    elif unit == 'hours':
        sched.every(interval).hours.do(run_bot, bot)
    elif unit == 'days':
        sched.every(interval).days.do(run_bot, bot)
    else:
        logger.warning(f"Unknown interval format: {run_every}, defaulting to 10 minutes")
        sched.every(10).minutes.do(run_bot, bot)

def parse_interval(run_every):
    parts = run_every.split()
    if len(parts) != 2:
        raise ValueError("Invalid run_every format. Expected '<number> <unit>'.")
    return int(parts[0]), parts[1]

def run_bot(bot):
    bot.run()

def run_scheduled_jobs():
    while True:
        sched.run_pending()
        time.sleep(1)
