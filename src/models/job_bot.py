import logging
from lib.database import ensure_table_exists, job_already_posted, save_posted_job


class JobBot:
    def __init__(self, name, sources, channels):
        self.name = name
        self.sources = sources
        self.channels = channels
        self.logger = logging.getLogger(self.name)
        
    @staticmethod
    def _get_table_name(channel_name, channel_uid):
        return f"{channel_name}_{channel_uid}".replace('@', '').replace('-', '_')
    
    def run(self):
        self.logger.info(f"Running job bot: {self.name}")
        for source, params in self.sources:
            jobs = source.fetch_jobs(**params)
            for job in jobs:
                for channel in self.channels:
                    table_name = self._get_table_name(channel.name, channel.uid)
                    ensure_table_exists(table_name)
                    if not job_already_posted(job.id, table_name):
                        channel.post_txt(job.message())
                        save_posted_job(job.id, table_name)
                        self.logger.info(f"Posted job {job.id} to channel {table_name}")
                    else:
                        self.logger.info(f"Job {job.id} already posted to channel {table_name}")


