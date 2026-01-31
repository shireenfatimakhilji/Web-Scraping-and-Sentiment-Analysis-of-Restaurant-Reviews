from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementNotInteractableException
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

scrape_csv = pd.read_csv('IlCortileRestaurant.csv')
scrape_csv = scrape_csv[:900]
review_json = pd.read_json('review_analysis.json').T
review_json.reset_index(drop=True, inplace=True)
review_data = pd.concat([scrape_csv, review_json], axis=1)

@app.route('/')
def displayReviews():
    reviews = []

    for colName, row in review_data.iterrows():
        review = {
            'name': row['name'],
            'city': row['city'],
            'total_reviews': row['total_reviews'],
            'food': row['food'],
            'staff': row['staff'],
            'overall_rating': row['overall_rating'],
            'food_rating': row['food_rating'],
            'service_rating': row['service_rating'],
            'ambience_rating': row['ambience_rating'],
            'date': row['date']
        }
        reviews.append(review)
    
    search_reviews = request.args.get('search', '').lower()

    search_filter = []
    for review in reviews:
        food_rev = review['food'].lower()
        staff_rev = review['staff'].lower()
        if search_reviews in food_rev or search_reviews in staff_rev:
            search_filter.append(review)

    return render_template('review_layout.html', reviews=search_filter)


def scrape_reviews(url):
    driver.get(url)

    title = driver.find_element(By.TAG_NAME, 'h1')
    print(title.text)
    print("\n")
    Title = ''.join(title.text.split())

    file = open(f"{Title}.csv", "a")
    file.write("overall_rating,date\n")
    file.close()

    while True:
        try:
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
            return Title
            break  # Exit the loop if there is any other error (element not found even after waiting, div present but no interactivity)


@app.route("/competitor_analysis", methods=["GET", "POST"])
def competitor_analysis():
    url = ""
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            Title = scrape_reviews(url)
            old = pd.read_csv("IlCortileRestaurant.csv")
            new = pd.read_csv(f"{Title}.csv")

            old_rating = old["overall_rating"][20:]
            new_rating = new["overall_rating"][20:]

            old_date = old["date"][20:]
            new_date = new["date"][20:]

            old_date = pd.to_datetime(old_date.str.replace('Dined on ', ''), format='%B %d %Y')
            new_date = pd.to_datetime(new_date.str.replace('Dined on ', ''), format='%B %d %Y')

            plt.figure(figsize=(12, 6))
            plt.plot(old_date, old_rating, label='competitor 1', color='green')
            plt.plot(new_date, new_rating, label='competitor 2', color='pink')
            plt.xlabel('Date')
            plt.ylabel('Overall Rating')
            plt.title('Rating trends over time')
            plt.legend()
            plt.savefig('graph.png')
            plt.close() 


    return render_template("competitor_analysis.html")

if __name__ == '__main__':
    app.run(debug=True)
