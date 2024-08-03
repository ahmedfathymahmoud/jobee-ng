import os
import yaml
from dotenv import load_dotenv

class Config:
    def __init__(self, config_file=None):
        load_dotenv()
        self.LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
        self.LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
        if config_file is None:
            config_file = os.path.join(os.path.dirname(__file__), 'config.yaml')
        self._load_yaml_config(config_file)
    def _load_yaml_config(self, config_file):
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)
        self.BOTS = self.config.get('bots', [])

    def get_linkedin_credentials(self):
        return self.LINKEDIN_EMAIL, self.LINKEDIN_PASSWORD

    def get_bots_config(self):
        return self.BOTS

config = Config()
