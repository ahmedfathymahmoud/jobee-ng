from linkedin_api import Linkedin
from config.settings import config

# Authenticate using any Linkedin account credentials
api = Linkedin('', '')

# GET a profile
#profile = api.get_profile('billy-g')


#print(profile)
# GET a profiles contact info
#contact_info = api.get_profile_contact_info('billy-g')
#print(contact_info)

# GET 1st degree connections of a given profile
# connections = api.get_profile_connections('1234asc12304')

"""Perform a LinkedIn search for jobs.

        :param keywords: Search keywords (str)
        :type keywords: str, optional
        :param companies: A list of company URN IDs (str)
        :type companies: list, optional
        :param experience: A list of experience levels, one or many of "1", "2", "3", "4", "5" and "6" (internship, entry level, associate, mid-senior level, director and executive, respectively)
        :type experience: list, optional
        :param job_type:  A list of job types , one or many of "F", "C", "P", "T", "I", "V", "O" (full-time, contract, part-time, temporary, internship, volunteer and "other", respectively)
        :type job_type: list, optional
        :param job_title: A list of title URN IDs (str)
        :type job_title: list, optional
        :param industries: A list of industry URN IDs (str)
        :type industries: list, optional
        :param location_name: Name of the location to search within. Example: "Kyiv City, Ukraine"
        :type location_name: str, optional
        :param remote: Filter for remote jobs, onsite or hybrid. onsite:"1", remote:"2", hybrid:"3"
        :type remote: list, optional
        :param listed_at: maximum number of seconds passed since job posting. 86400 will filter job postings posted in last 24 hours.
        :type listed_at: int/str, optional. Default value is equal to 24 hours.
        :param distance: maximum distance from location in miles
        :type distance: int/str, optional. If not specified, None or 0, the default value of 25 miles applied.
        :param limit: maximum number of results obtained from API queries. -1 means maximum which is defined by constants and is equal to 1000 now.
        :type limit: int, optional, default -1
        :param offset: indicates how many search results shall be skipped
        :type offset: int, optional
        :return: List of jobs
        :rtype: list
        """

jobs = api.search_jobs(
        #job_title=['HPC Engineer'],
        keywords='DevOps',
        location_name='France',
        limit=5,
        offset=0,
    )


for job in jobs:
    print(f'https://www.linkedin.com/jobs/view/{job['entityUrn'].split(':')[-1]}')