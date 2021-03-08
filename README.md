# 12-Mars-Web-Scraping

The main objective of this assignment was to use the Python library, BeautifulSoup to inspect the documents and scrape the necessary information from the provided URLs. I scraped the most recent headline from the NASA website, images of the surface of Mars and a table; which were then added to my own dashboard. Also, using Flask_PyMongo I was able to set up a mongo connection between the scraped data and the main python file. 
The repo consisits of a Jupyter Notebook, main app.py (to establish connection), 2nd app.py (to import bs) and a html (to show the dashboard).

## There were four URLs provided which were used to gether the information and visuals related to Mars:

## NASA Mars News
https://www.jpl.nasa.gov/images?search=&category=Mars

## JPL Mars Space Images - Featured Image
https://www.jpl.nasa.gov/images

## Mars Facts
https://space-facts.com/mars

## Mars Hemispheres
https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

Other imported libraries:

pandas

splinter

selenium

webdriver

ChromeDriverManager


