from src.factories.job_bot_factory import JobBotFactory
from config.settings import config
from lib.logging import setup_logging
from lib.schedule import schedule_bot, run_scheduled_jobs

logger = setup_logging()

def main():
    bots_config = config.get_bots_config()
    factory = JobBotFactory()

    for bot_config in bots_config:
        bot = factory.create_bot(bot_config)
        run_every = bot_config.get('run_every', '10 minutes')
        schedule_bot(bot, run_every)

    run_scheduled_jobs()

if __name__ == '__main__':
    logger.info("Starting job bot...")
    main()
    logger.info("Job bot finished.")