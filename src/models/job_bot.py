class JobBot:
    def __init__(self, name, sources, channels):
        self.name = name
        self.sources = sources
        self.channels = channels

    def run(self):
        for source, params in self.sources:
            jobs = source.fetch_jobs(**params)
            for job in jobs:
                for channel in self.channels:
                    print(job.message())
                    channel.post_message(job.message())



