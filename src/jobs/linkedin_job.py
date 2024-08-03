from src.models.job import Job
from datetime import datetime


class LinkedInJob(Job):
    def __init__(self, id, api):
        super().__init__(id)
        self.API= api

    def _get_job_details(self):
        job_details=self.API.get_job(self.id)
        return job_details

    def message(self):
        job=self._get_job_details()
        ts = int(job['listedAt'])/1000
        post_time = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
        if 'com.linkedin.voyager.jobs.OffsiteApply' in job["applyMethod"]:
            apply_method='company website'
            apply_url=  job["applyMethod"]["com.linkedin.voyager.jobs.OffsiteApply"]["companyApplyUrl"]
        elif 'com.linkedin.voyager.jobs.ComplexOnsiteApply' in job["applyMethod"]:
            apply_method='easy apply'
            apply_url=  f'https://www.linkedin.com/jobs/view/{self.id}'
        elif 'com.linkedin.voyager.jobs.SimpleOnsiteApply' in job["applyMethod"]:
            apply_method='one click easy apply'
            apply_url=  f'https://www.linkedin.com/jobs/view/{self.id}'
        else:
            apply_method='unknown'
            apply_url=f'https://www.linkedin.com/jobs/view/{self.id}'
            
        m = f'''
Title: {job["title"]}
Location: {job["formattedLocation"]}
Remote: {job["workRemoteAllowed"]}
Apply Method: {apply_method}
Apply URL: {apply_url}
Posted at: {post_time}

Linkedin post: https://www.linkedin.com/jobs/view/{self.id}
'''
        return m
