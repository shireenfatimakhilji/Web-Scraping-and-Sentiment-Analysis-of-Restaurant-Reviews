from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import matplotlib.pyplot as plt
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementNotInteractableException

# Initialize web driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open restaurant page
url = "https://www.opentable.com/r/blue-fire-restaurant-elmwood-park?originId=d35fc532-445e-493e-a4c7-b9bd50873323&corrid=d35fc532-445e-493e-a4c7-b9bd50873323&avt=eyJ2IjoyLCJtIjoxLCJwIjoxLCJzIjowLCJuIjowfQ"
driver.get(url)

title = driver.find_element(By.TAG_NAME, 'h1')
print(title.text)
print("\n")
Title = ''.join(title.text.split())

file = open(f"{Title}.csv", "a")
file.write("overall_rating,date\n")
file.close()

# Function to scrape reviews from the current webpage
def scraping_reviews():
    overall_rating = driver.find_elements(By.XPATH, './/div/ol/li[1]/span')
    dates = driver.find_elements(By.CLASS_NAME, 'iLkEeQbexGs-') 
    file = open(f"{Title}.csv", "a")
    for i in range(len(dates)):
        # printing review
        print(overall_rating[i].text)
        date = dates[i].text.replace(',', '')
        print(date)
        print("\n")

        # saving review in a csv
        file.write(f'{overall_rating[i].text},{date}\n')

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


old = pd.read_csv("IlCortileRestaurant.csv")
new = pd.read_csv(f"{Title}.csv")

old_rating = old["overall_rating"][20:]
new_rating = new["overall_rating"][20:]

old_date = old["date"][20:]
new_date = new["date"][20:]

old_date = pd.to_datetime(old_date.str.replace('Dined on ', ''), format='%B %d %Y')
new_date = pd.to_datetime(new_date.str.replace('Dined on ', ''), format='%B %d %Y')

plt.figure(figsize=(12, 6))
plt.plot(old_date, old_rating, label='competitor 1', color='orange')
plt.plot(new_date, new_rating, label='competitor 2', color='red')
plt.xlabel('Date')
plt.ylabel('Overall Rating')
plt.title('Date vs Rating')
plt.legend()
plt.grid()
plt.show()
