from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

# Function to initialize a Chrome WebDriver
def initialize_driver():
    return webdriver.Chrome()

# Function to navigate to the specified search engine URL
def navigate_to_search_engine(driver, search_engine_url):
    driver.get(search_engine_url)
    sleep(2)

# Function to perform a search using the provided query
def perform_search(driver, query):
    # XPaths for search box and search button
    search_box_xPath = "//*[@id='q']"
    search_button_xPath = "//*[@id='send_search']"

    # Find and interact with the search box
    search_box = driver.find_element(By.XPATH, search_box_xPath)
    sleep(1)
    search_box.click()
    sleep(1)
    search_box.send_keys(query)

    # Find and click the search button
    search_button = driver.find_element(By.XPATH, search_button_xPath)
    sleep(1)
    search_button.click()
    sleep(10)

# Function to extract URLs from search results on multiple pages
def extract_urls(driver, num_pages):
    all_urls = []

    for i in range(num_pages):
        # XPath for URL elements in the search results
        urls_xPath = "//*[@id='urls']/article/a/span[1]/span"

        # Find all URL elements on the current page
        url_elements = driver.find_elements(By.XPATH, urls_xPath)
        all_urls.extend(url_element.text for url_element in url_elements)

        sleep(5)

        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)

        # Click on the next page button
        if i >= 1:
            next_page_button_xPath = "//*[@id='pagination']/div/form[{}]/input[8]".format(i + 1)
        else:
            next_page_button_xPath = "//*[@id='pagination']/div/form[1]/input[8]"

        next_page_button = driver.find_element(By.XPATH, next_page_button_xPath)
        next_page_button.click()
        sleep(6)  # Adjust this wait time based on the actual loading time of the next page

    return all_urls

# Function to print extracted URLs
def print_urls(urls):
    print("Search Results:")
    for i, url in enumerate(urls, start=1):
        print(f"{i}. {url}")

# Function to close the WebDriver
def close_driver(driver):
    driver.quit()

# Main function to perform search and scrape URLs
def search_and_scrape(search_engine_url, search_query, num_pages=5):
    driver = initialize_driver()

    try:
        navigate_to_search_engine(driver, search_engine_url)
        perform_search(driver, search_query)

        urls = extract_urls(driver, num_pages)
        print_urls(list(set(urls)))

    finally:
        close_driver(driver)

# Main block to execute the search_and_scrape function
if __name__ == "__main__":
    search_engine_url = "https://search.broker/search"
    search_query = 'badam pista inurl:contact intitle:contact "+91"'

    search_and_scrape(search_engine_url, search_query)