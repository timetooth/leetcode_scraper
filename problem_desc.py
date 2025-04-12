"""
This script scrapes the HTML description of LeetCode problems using Selenium for browser automation
and BeautifulSoup for parsing. The scraped data is stored in a Pandas DataFrame.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd


def scrape(row):
    """
    Scrapes the description content of a specific LeetCode problem.

    Args:
        row (pd.Series): A row containing the 'titleSlug' field.

    Returns:
        str: The HTML content of the problem's description.
    """
    url = 'https://leetcode.com/problems/' + row['titleSlug'] + '/description/'
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    try:
        driver.get(url)
        driver.implicitly_wait(10)
        element = driver.find_element(By.CSS_SELECTOR, 'div[data-track-load="description_content"]')
        html_content = element.get_attribute('outerHTML')
        return str(html_content)
    except Exception as e:
        print(f"{url} | An error occurred")
        print(f"ERROR: {e}")
        return ''
    finally:
        driver.quit()



questions = pd.read_csv('./problem_set.csv')

"""find the problem_csv on Hugging face"""

questions = questions[:5]
questions['description'] = questions.apply(scrape, axis=1)

print(questions.head(10))