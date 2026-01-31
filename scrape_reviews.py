from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementNotInteractableException

# Initialize web driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open restaurant page
url = "https://www.opentable.com/il-cortile-restaurant?corrid=6730c40d-e58b-4e0e-97d6-b5a76b288058&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2024-11-30T19%3A00%3A00"
driver.get(url)

title = driver.find_element(By.TAG_NAME, 'h1')
print(title.text)
print("\n")
Title = ''.join(title.text.split())

file = open(f"{Title}.csv", "a")
file.write("name,city,total_reviews,review_content,overall_rating,food_rating,service_rating,ambience_rating,date\n")
file.close()

# Function to scrape reviews from the current webpage
def scraping_reviews():
    name = driver.find_elements(By.CLASS_NAME, '_1p30XHjz2rI-.C7Tp-bANpE4-')
    city = driver.find_elements(By.CLASS_NAME, 'POyqzNMT21k-.C7Tp-bANpE4-')
    total_reviews = driver.find_elements(By.CLASS_NAME, '_4je3Yf1hhfo-._7aCjEplNYVQ-')
    review_content = driver.find_elements(By.CLASS_NAME, '_6rFG6U7PA6M-')
    overall_rating = driver.find_elements(By.XPATH, './/div/ol/li[1]/span')
    food_rating = driver.find_elements(By.XPATH, './/div/ol/li[2]/span')
    service_rating = driver.find_elements(By.XPATH, './/div/ol/li[3]/span')
    ambience_rating = driver.find_elements(By.XPATH, './/div/ol/li[4]/span')
    dates = driver.find_elements(By.CLASS_NAME, 'iLkEeQbexGs-') 
    file = open(f"{Title}.csv", "a")
    for i in range(len(dates)):
        # printing review
        print(name[i].text)
        print(city[i].text)
        print(total_reviews[i].text)
        review = review_content[i].text.replace(',', '').replace(';', '').replace('\n', '').replace('Read more', '')
        print(review)
        print(overall_rating[i].text)
        print(food_rating[i].text)
        print(service_rating[i].text) 
        print(ambience_rating[i].text)
        date = dates[i].text.replace(',', '')
        print(date)
        print("\n")

        # saving review in a csv
        file.write(f'{name[i].text},{city[i].text},{total_reviews[i].text},"{review}",{overall_rating[i].text},{food_rating[i].text},{service_rating[i].text},{ambience_rating[i].text},{date}\n')

    file.close()

while True:
    try:
        # Call function to scrape reviews from current webpage
        scraping_reviews()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Go to the next page"]'))
        )

        # Find the next button and store it
        next_button = driver.find_element(By.XPATH, '//*[@aria-label="Go to the next page"]')

        # CLick the next button
        next_button.click()

        time.sleep(2)  # Sleep to wait for the page to load

    except StaleElementReferenceException:
        continue  # If element not found (could happen due to reloading or refreahing of page)

    except (TimeoutException, ElementNotInteractableException):
        break  # Exit the loop if there is any other error (element not found even after waiting, div present but no interactivity)
