from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {"executable_path": "C:/Users/Scott Proveucher/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    # Initialize the browser
    browser = init_browser()

    ### Visit NASA url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the first new title
    title_results = soup.find_all('div', class_='content_title')
    first_title = title_results[0].text

    # Get the first paragraph
    paragraph_results = soup.find_all('div', class_='article_teaser_body')
    first_paragraph = paragraph_results[0].text

    ## Visit image_url
    browser = init_browser()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Find featured image url
    featured_image_url2 = 'https://d2pn8kiwq2w21t.cloudfront.net/images/jpegPIA23727.width-768.jpg'

    ##Visit the table_url
    browser = init_browser()
    
    # Scrape the table data from page
    tables = pd.read_html('https://space-facts.com/mars/')
    
    # Turn into a DataFrame
    mars_df = tables[0]

    # Rename columns
    mars_df.columns=['Statistics', '']

    # Reset index
    mars_df.set_index('Statistics', inplace=True)

    # Convert table to html
    mars_statistics = mars_df.to_html(header=True, index=True)

    ### Visit the astrogeology page and scrape info on the Mars' hemispheres ###
    
    # Initialize the browser
    browser = init_browser()

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Create an empty list to store hemisphere names
    hemisphere_names = []

    # Search for image titles (hemisphere names)
    hemispheres = soup.find_all('div', class_='collapsible results')
    names = hemispheres[0].find_all("h3")

    # Add hemisphere names to the list
    for name in names:
        hemisphere_names.append(name.text.strip('Enhanced'))
    
    # Create empty list to store image urls
    links = []

    # Locate image links
    urls = soup.find_all("div", class_="item")

    # Add base link to image links and append to the list
    for url in urls:
        hemis_links = url.find('a')['href']
        path = 'https://astrogeology.usgs.gov' + hemis_links
        links.append(path)
    
    # Finding urls to full sized images for each hemisphere
    image_url = []

    # Click each image link 
    for link in links:
        browser.visit(link)
        html = browser.html
        soup = bs(html, 'html.parser')
    
        # Find full jpgs
        url = soup.find_all('img', class_='wide-image')
     
        full_urls = url[0]['src']
        
        # Add base link to image links and append to the list
        final_path = 'https://astrogeology.usgs.gov' + full_urls
       
        image_url.append(final_path)

    # Zip lists
    hemis_zip = zip(hemisphere_names, image_url)

    # Ceate a new list to store dictionaries
    hemisphere_image_urls = []

    # Add name and url image lists to dictionaries
    for name,img in hemis_zip:
        hemispheres_dict = {}
    
        # Add hemisphere name to dictionary
        hemispheres_dict['hemisphere_names'] = name
    
        # Add image url to dictionary
        hemispheres_dict['image_url'] = img
     
        # Append the list with dictionaries
        hemisphere_image_urls.append(hemispheres_dict)
 
    # Store all mars data in the dictionary
    mars_data = {
        "first_title": first_title,
        "first_paragraph": first_paragraph,
        "featured_image_url2": featured_image_url2,
        "mars_statistics": mars_statistics,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Return results
    return mars_data