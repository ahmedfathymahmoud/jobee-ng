import sqlite3
from scratch.utils import *
from config.settings import config


if __name__ == "__main__":
    
    conn = sqlite3.connect('jobs.db')
    create_table(conn)

    bots = config.get_bots_config()
    for bot_config in bots:
        destination = bot_config['to']
        bot = get_bot(destination)

        for source in bot_config['from']:
            for source_name, params in source.items():
                source = get_source(source_name)
                jobs = source.get_jobs(**params)
                for job in jobs:
                    job_id=job['entityUrn'].split(':')[-1]
                    print(generate_message(source_name, job) )
                    if not job_exists(conn, job_id):
                        insert_job(conn, job_id)
                        message = generate_message(source_name, job)
                        print(message)
                        bot.post_message(message)    
