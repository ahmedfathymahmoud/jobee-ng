from linkedin_api import Linkedin
from config.settings import config

class LinkedinAPI:
    def __init__(self):
        email, password = config.get_linkedin_credentials()
        self.api = Linkedin(email, password)

    def get_jobs(self, **kwargs):
        jobs = self.api.search_jobs(**kwargs)
        return jobs
