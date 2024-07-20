#used for forming the dataset

import requests
from bs4 import BeautifulSoup
import csv

def scrape_reviews_on_page(page_url):
    # Sending a HTTP GET request to the page
    response = requests.get(page_url)
    
    # Checking if the request was successful
    if response.status_code == 200:
        # Parsing the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Finding the section containing reviews
        reviews_section = soup.find('div', class_='rc-ReviewsContainer')
        
        if reviews_section:
            # Finding all review elements
            reviews = reviews_section.find_all('div', class_='reviewText')
            
            # Finding all rating elements
            ratings = reviews_section.find_all('div', class_='_1mzojlvw')
            
            if reviews and ratings:
                # Return reviews and ratings
                return zip(reviews, ratings)
    return None
#scraper for consecutive pages
def scrape_coursera_reviews(course_url, output_file):
    page_num = 1
    
    while True:
        
        url = f"{course_url}?page={page_num}"
        
        # Scrape reviews on the current page
        reviews_and_ratings = scrape_reviews_on_page(url)
        
        if reviews_and_ratings:
            # open CSV file
            with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write each review and rating to CSV
                for review, rating in reviews_and_ratings:
                    review_text = review.get_text().strip()
                    filled_stars = rating.find_all('svg', style='fill:#F2D049;height:14px;width:14px;margin-right:2px;vertical-align:text-bottom')
                    rating_count = len(filled_stars)
                    writer.writerow([rating_count, review_text])
        else:
            print("No reviews found on this page or failed to retrieve page.")
            break
        
        # Moving to the next page
        page_num += 1


course_url = "https://www.coursera.org/learn/deploy-and-maintain-power-bi-assets-and-capstone-project/reviews"
output_file = "coursera_reviews.csv"
scrape_coursera_reviews(course_url, output_file)

## scraper for single page
# import requests
# from bs4 import BeautifulSoup
# import csv

# def scrape_coursera_reviews(course_url, output_file):
#     # Send a GET request to the Coursera course page
#     response = requests.get(course_url)
    
#     # Check if the request was successful
#     if response.status_code == 200:
#         # Parse the HTML content of the page
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         # Find the section containing reviews
#         reviews_section = soup.find('div', class_='rc-ReviewsContainer')
        
#         if reviews_section:
#             # Find all review elements
#             reviews = reviews_section.find_all('div', class_='reviewText')
            
#             # Find all rating elements
#             ratings = reviews_section.find_all('div', class_='_1mzojlvw')
            
#             if reviews and ratings:
#                 # Write data to CSV file
#                 with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
#                     writer = csv.writer(csvfile)
#                     # Write each review and rating to CSV
#                     for review, rating in zip(reviews, ratings):
#                         review_text = review.get_text().strip()
#                         filled_stars = rating.find_all('svg', style='fill:#F2D049;height:14px;width:14px;margin-right:2px;vertical-align:text-bottom')
#                         rating_count = len(filled_stars)
#                         writer.writerow([rating_count, review_text])
#             else:
#                 print("No reviews found for this course.")
#         else:
#             print("Reviews section not found.")
#     else:
#         print("Failed to retrieve course page.")

# # Example usage
# course_url = "https://www.coursera.org/learn/assess-for-success/reviews?page=1&star=2"
# output_file = "coursera_reviews.csv"
# scrape_coursera_reviews(course_url, output_file)
