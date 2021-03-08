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
    

        hemisphere_image_urls = [
    {"title": "Cerberus Hemisphere", "imgage_url": "https://astrogeology.usgs.gov/cache/images/39d3266553462198bd2fbc4d18fbed17_cerberus_enhanced.tif_thumb.png"},
    {"title": "Schiaparelli Hemisphere", "imgage_url": "https://astrogeology.usgs.gov/cache/images/08eac6e22c07fb1fe72223a79252de20_schiaparelli_enhanced.tif_thumb.png"},
    {"title": "Syrtis Major Hemisphere", "imgage_url": "https://astrogeology.usgs.gov/cache/images/55a0a1e2796313fdeafb17c35925e8ac_syrtis_major_enhanced.tif_thumb.png"},
    {"title": "Valles Marineris Hemisphere", "imgage_url": "https://astrogeology.usgs.gov/cache/images/4e59980c1c57f89c680c0e1ccabbeff1_valles_marineris_enhanced.tif_thumb.png"},]

 
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