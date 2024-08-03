from src.models.source import Source
from src.models.channel import Channel
from src.models.job_bot import JobBot
import importlib

class JobBotFactory:
    def create_source(self, source_config):
        source_type = list(source_config.keys())[0]
        params = source_config[source_type]
        module_name = f"src.sources.{source_type.lower()}_source"
        class_name = f"{source_type}Source"
        source_module = importlib.import_module(module_name)
        source_class = getattr(source_module, class_name)
        return source_class(), params


    def create_channel(self, channel_config):
        channel_type = list(channel_config.keys())[0]
        params = channel_config[channel_type]
        module_name = f"src.channels.{channel_type.lower()}_channel"
        class_name = f"{channel_type.capitalize()}Channel"
        channel_module = importlib.import_module(module_name)
        channel_class = getattr(channel_module, class_name)
        return channel_class(**params)

    def create_bot(self, bot_config):
        name = bot_config['name']
        sources = [self.create_source(src) for src in bot_config['from']]
        channels = [self.create_channel(ch) for ch in bot_config['to']]
        return JobBot(name, sources, channels)
