from src.factories.job_bot_factory import JobBotFactory
import yaml
from config.settings import config
from lib.logging import setup_logging

logger = setup_logging()

def main():

    factory = JobBotFactory()
    bots_config = config.get_bots_config()
    for bot_config in bots_config:
        bot = factory.create_bot(bot_config)
        bot.run()




logger.info("Starting job bot...")
main()
logger.info("Job bot finished.")
