import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv
import json


def google_search_results(search_query, num_results):
    service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # For google
    # driver.get(f"https://www.google.com/search?q={search_query}&num={num_results}")
    # For Google News
    driver.get(f"https://news.google.com/search?q={search_query}&num={num_results}")
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # For google
    # links = []
    #for result in soup.find_all('div', {'class': 'tF2Cxc'}):
    #    link = result.find('a', {'jsname': 'UWckNb'})['href']
    #    links.append(link)
    #For Google News
    links = []
    # Extract the links
    div_elements = driver.find_elements(By.CSS_SELECTOR, "div.XlKvRb")
    for div in div_elements:
        link_elements = div.find_elements(By.CSS_SELECTOR, "a.WwrzSb")
        for link_element in link_elements:
            if link_element and len(links) < num_results:
                full_url = link_element.get_attribute('href')
                links.append(full_url)

    driver.quit()
    return links


def page_text(url):
    service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    wait = WebDriverWait(driver, 2)

    # Try to handle cookie pop-up
    try:
        # First, try finding a button that contains the text "I Accept"
        accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "I Accept")]')))
        accept_button.click()
    except TimeoutException:
        try:
            # If that fails, try finding a button with the title "I Accept"
            accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="I Accept"]')))
            accept_button.click()
        except TimeoutException:
            print("No standard cookie pop-up found.")

    # Extract text from the page
    paragraphs = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'p')))
    page_text = ' '.join([paragraph.text for paragraph in paragraphs])

    driver.quit()
    return page_text


df = pd.read_csv(r'C:\Users\HP\PycharmProjects\BigData\kyc.csv')
df['Name'] = df['Name'].str.title()

split_names = df['Name'].str.split(' ', n=1, expand=True)
df['First Name'] = split_names[0]
df['Last Name'] = split_names[1]
df_unique = df.drop_duplicates(subset=['First Name'])
df_unique = df_unique['First Name']
df_unique = df_unique[501:750]
url_json = {}

for name in df_unique:
    search_query = "wildlife trafficking "+name
    num_results = 5
    urls = google_search_results(search_query, num_results)
    url_data = {}
    for url in urls:
        print(f"URL: {url}")
        try:
            text = page_text(url)
            if text != '':
                url_data[url] = text
            print(f"Page Text: {text[:5000]}")
        except Exception as e:
            print(f"Error occurred: {e}")
        print("\n")
    url_json[name] = url_data

url_json_string = json.dumps(url_json, indent=4)

# Print the JSON string
print(url_json_string)

# Optionally, save to a file
with open('output.json', 'w') as file:
    file.write(url_json_string)

#url_dict = [{'URL': url, 'Page_text': text} for url, text in url_data.items()]

#with open('test_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
#    writer = csv.DictWriter(csvfile, fieldnames=['URL', 'Page_text'])
#    writer.writeheader()
#    writer.writerows(url_dict)