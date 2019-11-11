from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from time import sleep
from bs4 import BeautifulSoup
from configparser import ConfigParser
from utility import scroll_down, get_matching_links, slow_down, JobParser
import re



SLEEP_INTERVAL = 5
driver = webdriver.Chrome("/Users/programming/PycharmProjects/liscrape/chromedriver")

@slow_down
def login():
    sleep(SLEEP_INTERVAL)
    # Reads `config.ini`
    config = ConfigParser()
    config.read('config.ini')
    username = config.get('LinkedIn', 'username')
    password = config.get('LinkedIn', 'password')

    # Goes to login page
    driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")

    # Enters username
    username_element = driver.find_element_by_id('username')
    username_element.clear()
    username_element.send_keys(username)

    # Enters password
    password_element = driver.find_element_by_id('password')
    password_element.clear()
    password_element.send_keys(password)

    # Presses button
    login_button = driver.find_element_by_xpath('//*[@id="app__container"]/main/div/form/div[3]/button')
    login_button.send_keys(Keys.RETURN)
    sleep(SLEEP_INTERVAL)

    if "Let's do a quick security check" in driver.page_source:
        if input("Please solve the captcha, then enter anything to continue:\n>>> "):
            pass

@slow_down
def search_jobs(query, location) -> str:
    sleep(SLEEP_INTERVAL)
    driver.get("https://www.linkedin.com/jobs/")

    # Enters query
    keyword_search = driver.find_element_by_class_name('jobs-search-box__text-input')
    keyword_search.clear()
    keyword_search.send_keys(query)

    # Enters location
    location_search = driver.find_element_by_xpath('//*[@id="jobs-search-box-location-id-ember33"]')
    location_search.clear()
    location_search.send_keys(location)

    # Presses button
    location_search.send_keys(Keys.RETURN)
    sleep(SLEEP_INTERVAL)

    # Returns url
    return driver.current_url

@slow_down
def scrape_links(url, num_pages=1) -> set:
    sleep(SLEEP_INTERVAL)
    links = set()
    pattern = re.compile('/jobs/view/\S*')
    driver.get(url)

    for page in range(num_pages):
        # Find job listing element & then scroll down to load all listings
        job_listings = driver.find_element_by_xpath('//*[@id="ember4"]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]')
        scroll_down(job_listings)
        sleep(2)

        # Get page source (HTML) and then get job links from that
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        matching_links = get_matching_links(pattern, soup)
        links.update(matching_links)

        # Go to the next page
        try:
            next_page = driver.find_element_by_css_selector('li.active + li button')
            next_page.click()
        except (NoSuchElementException, ElementClickInterceptedException):
            break

    return links

@slow_down
def scrape_job_description(url):
    # Navigates to job url
    driver.get(url)

    # Clicks on the "See more" button to display full text
    try:
        see_more_button = driver.find_element_by_css_selector("button[data-control-name='see_more']")
        see_more_button.click()
    except NoSuchElementException:
        pass

    # Gets HTML from page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    uuid = url[35:].split('/')[0]

    # Parse the HTML into an object
    job = JobParser(soup, job_id=uuid)
    return job







if __name__ == '__main__':
    login()
    link = search_jobs('Data Analyst', 'Los Angeles, California')
    job_links = scrape_links(link, num_pages=2)

    for j in job_links:
        sleep(3)
        scrape_job_description(j)







