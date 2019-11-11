from selenium.webdriver.common.keys import Keys
import functools
import time

def scroll_down(element):
    """
    Given an element, attempts to scroll down using `PAGE DOWN`.
    Used in this library to ensure all dynamically loaded content is added.
    """
    for x in range(10):
        element.send_keys(Keys.PAGE_DOWN)

def get_matching_links(pattern, soup):
    """
    Gets all links that match a regex pattern
    """
    links = set()

    for link in soup.find_all('a', href=True):
        if pattern.match(link['href']):
            job_link = "https://www.linkedin.com%s" % link['href']
            links.add(job_link)

    return links

def slow_down(func, seconds=1):
    """
    Used as a decorator to slow down scraping functions
    Copied from "https://realpython.com/primer-on-python-decorators/"
    """
    @functools.wraps(func)
    def wrapper_slow_down(*args, **kwargs):
        time.sleep(seconds)
        return func(*args, **kwargs)

    return wrapper_slow_down

class JobParser:
    base_url = "https://www.linkedin.com/jobs/view/"

    def __init__(self, soup, job_id=0):
        self.soup = soup
        self.job_id = job_id
        self.url = self.base_url + str(job_id)

    @property
    def title(self):
        try:
            title = self.soup.find(name='h1', attrs={'class': 'jobs-top-card__job-title t-24'}).string.strip()
        except AttributeError:
            title = ''
        return title

    @property
    def description(self):
        try:
            description = self.soup.find(name='div', id='job-details')
            description = description.text.replace(',', '').replace('\n', ' ').encode('utf-8').strip()
        except AttributeError:
            description = ''
        return description

    @property
    def location(self):
        try:
            location = self.soup.find(name='span', attrs={'class': 'jobs-top-card__bullet'}).string.strip()
        except AttributeError:
            try:
                location = self.soup.find(name='a', attrs={
                    'class': 'jobs-top-card__exact-location t-black--light link-without-visited-state'}).string.strip()
            except AttributeError:
                location = ''
        return location

    @property
    def experience_level(self):
        try:
            experience_level = self.soup.find(name='p', attrs={'class': 'jobs-box__body js-formatted-exp-body'}).string.strip()
        except AttributeError:
            experience_level = ''
        return experience_level

    @property
    def industries(self):
        try:
            industries = self.soup.find(name='ul', attrs={'class': 'jobs-box__list jobs-description-details__list js-formatted-industries-list'})
            industries = [child.string.strip() for child in industries.children if child.string.strip()]
        except AttributeError:
            industries = []
        return industries

    @property
    def employment_type(self):
        try:
            employment_type = self.soup.find(name='p', attrs={'class': 'jobs-box__body js-formatted-employment-status-body'}).string.strip()
        except AttributeError:
            employment_type = 'Not applicable'
        return employment_type

    @property
    def job_functions(self):
        try:
            job_functions = self.soup.find(name='ul', attrs={'class': 'jobs-box__list jobs-description-details__list js-formatted-job-functions-list'})
            job_functions = [child.string.strip() for child in job_functions.children if child.string.strip()]
        except AttributeError:
            job_functions = ''
        return job_functions

    @property
    def company(self):
        # TODO: Return url too
        try:
            company = self.soup.find(name='a', attrs={'class': 'jobs-top-card__company-url ember-view'}).string.strip()
        except AttributeError:
            company = ''
        return company









