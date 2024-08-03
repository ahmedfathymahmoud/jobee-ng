from src.models.source import Source
from src.jobs.linkedin_job import LinkedInJob
from config.settings import config
from linkedin_api import Linkedin
from urllib.parse import quote, urlencode


class LinkedinMod(Linkedin):

    def search_jobs(
        self,
        keywords=None,
        companies=None,
        experience=None,
        job_type=None,
        job_title=None,
        industries=None,
        location_name=None,
        geoId=None,
        remote=None,
        listed_at=24 * 60 * 60,
        distance=None,
        limit=-1,
        offset=0,
        **kwargs,
    ):
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
        count = Linkedin._MAX_SEARCH_COUNT
        if limit is None:
            limit = -1

        query = {"origin": "JOB_SEARCH_PAGE_QUERY_EXPANSION"}
        if geoId:
            query["locationUnion"] = f'(geoId:{geoId})'
        if keywords:
            query["keywords"] = "KEYWORD_PLACEHOLDER"
        if location_name:
            query["locationFallback"] = "LOCATION_PLACEHOLDER"

        # In selectedFilters()
        query["selectedFilters"] = {}
        if companies:
            query["selectedFilters"]["company"] = f"List({','.join(companies)})"
        if experience:
            query["selectedFilters"]["experience"] = f"List({','.join(experience)})"
        if job_type:
            query["selectedFilters"]["jobType"] = f"List({','.join(job_type)})"
        if job_title:
            query["selectedFilters"]["title"] = f"List({','.join(job_title)})"
        if industries:
            query["selectedFilters"]["industry"] = f"List({','.join(industries)})"
        if distance:
            query["selectedFilters"]["distance"] = f"List({distance})"
        if remote:
            query["selectedFilters"]["workplaceType"] = f"List({','.join(remote)})"

        query["selectedFilters"]["timePostedRange"] = f"List(r{listed_at})"

        # Query structure:
        # "(
        #    origin:JOB_SEARCH_PAGE_QUERY_EXPANSION,
        #    keywords:marketing%20manager,
        #    locationFallback:germany,
        #    selectedFilters:(
        #        distance:List(25),
        #        company:List(163253),
        #        salaryBucketV2:List(5),
        #        timePostedRange:List(r2592000),
        #        workplaceType:List(1)
        #    ),
        #    spellCorrectionEnabled:true
        #  )"

        query = (
            str(query)
            .replace(" ", "")
            .replace("'", "")
            .replace("KEYWORD_PLACEHOLDER", keywords or "")
            .replace("LOCATION_PLACEHOLDER", location_name or "")
            .replace("GEOID_PLACEHOLDER",  f"List({geoId})"or "")
            .replace("{", "(")
            .replace("}", ")")
        )
        print(query)
        results = []
        while True:
            # when we're close to the limit, only fetch what we need to
            if limit > -1 and limit - len(results) < count:
                count = limit - len(results)
            default_params = {
                "decorationId": "com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-174",
                "count": count,
                "q": "jobSearch",
                "query": query,
                "start": len(results) + offset,
            }

            res = self._fetch(
                f"/voyagerJobsDashJobCards?{urlencode(default_params, safe='(),:')}",
                headers={"accept": "application/vnd.linkedin.normalized+json+2.1"},
            )
            data = res.json()

            elements = data.get("included", [])
            new_data = [
                i
                for i in elements
                if i["$type"] == "com.linkedin.voyager.dash.jobs.JobPosting"
            ]
            # break the loop if we're done searching or no results returned
            if not new_data:
                break
            # NOTE: we could also check for the `total` returned in the response.
            # This is in data["data"]["paging"]["total"]
            results.extend(new_data)
            if (
                (-1 < limit <= len(results))  # if our results exceed set limit
                or len(results) / count >= Linkedin._MAX_REPEATED_REQUESTS
            ) or len(elements) == 0:
                break

            self.logger.debug(f"results grew to {len(results)}")

        return results



class LinkedInSource(Source):
    def __init__(self):
        email, password = config.get_linkedin_credentials()
        self.api = LinkedinMod(email, password)

    def fetch_jobs(self, **kwargs):
        jobs_data = self.api.search_jobs(**kwargs)
        job_ids = [job['entityUrn'].split(':')[-1] for job in jobs_data]
        return [LinkedInJob(job_id, self.api) for job_id in job_ids]
