from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json
# Path to ChromeDriver
driver_path = './chromedriver.exe'  # Make sure this path is correct

# Initialize the WebDriver with updated syntax for Selenium 4
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

# Go to the IMDb "Most Popular Movies" page
url = 'https://www.imdb.com/chart/moviemeter/?ref_=chtbo_ql_2'
driver.get(url)

# Scroll to the bottom of the page to load all movies
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "ipc-metadata-list-summary-item")]')))

# Find all the movie list items
movies = driver.find_elements(By.XPATH, '//li[contains(@class, "ipc-metadata-list-summary-item")]')

# List to hold movie data
movies_data = []

# Loop through each movie list item
for movie in movies:
    try:
        # Extract movie name
        name = movie.find_element(By.XPATH, './/h3').text
        print(name)
        #  ranking contains cli-meter-title-header and then extract the aria label from the span
        # Find the element with class "cli-meter-title-header"
        ranking_element = movie.find_element(By.XPATH, './/*[contains(@class, "cli-meter-title-header")]')
        
        # Find the span inside it and get its aria-label
        ranking_movement_span = ranking_element.find_element(By.TAG_NAME, "span")
        ranking_movement = ranking_movement_span.get_attribute("aria-label")

        print(ranking_movement)
        
        # meta data
        
        try:
            meta_data = movie.find_element(By.XPATH, './/*[contains(@class, "cli-title-metadata")]')
            meta_data_list = meta_data.find_elements(By.TAG_NAME, "span")
            print(meta_data_list[0].text, meta_data_list[1].text, meta_data_list[2].text)
        except:
            print("Error: Could not find meta data for movie. Skipping...")
            meta_data_list = []
        
        if meta_data_list:
            movies_data.append({
                "name": name,
                "ranking_movement": ranking_movement,
                "meta_data": {
                    "release_date": meta_data_list[0].text,
                    "runtime": meta_data_list[1].text,
                    "genre": meta_data_list[2].text
                }
            })
        else:
            movies_data.append({
                "name": name,
                "ranking_movement": ranking_movement,
                "meta_data": "N/A",
            })


    except NoSuchElementException:
        print(f"Error: Could not find all elements for movie. Skipping...")

# Print the extracted data
for movie in movies_data:
    print(movie)
    
# Save the data to a JSON file
with open('movies.json', 'w') as f:
    json.dump(movies_data, f)
    

# Close the browser once done
driver.quit()
