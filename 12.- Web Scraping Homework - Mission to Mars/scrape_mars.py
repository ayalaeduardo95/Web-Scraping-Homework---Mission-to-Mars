# Dependencies
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests
from splinter import Browser
import pandas as pd
import pymongo

# Mongo Setup

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars 

# Chrome Driver
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

# Scrape

def scrape():
    browser = init_browser()
    collection.drop()

    # NASA Mars News
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    news = browser.html
    news_soup = bs(news,'lxml')
    news_title = news_soup.find("div",class_="content_title").text
    news_p = news_soup.find("div", class_="rollover_description_inner").text

    # JPL Mars Space Images - Featured Image
    # URL
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    html = browser.html
    soup = bs(html, "html.parser")
    # Retrieval of Image
    jpl = "jpl.nasa.gov"
    image = soup.find_all("a", id="full_image")
    image = jpl + image[0]["data-fancybox-href"]
    # Image
    image

    # Mars Facts
    # URL
    MF_url = 'https://space-facts.com/mars/'
    browser.visit(MF_url)
    # Table of Facts about Mars
    facts = pd.read_html(MF_url)
    facts[0]
    # Creating a DF out of the table data
    Facts_df = facts[0]
    Facts_df
    # Converting to HTML
    Facts_HTML = Facts_df.to_html(header=False, index=False)
    Facts_HTML

    # Mars Hemispheres
    # Mars Hemispheres URL
    MH_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(MH_url)
    # BS Mars Hemispheres
    MH_url = browser.html
    print(MH_url)

    mh_soup = bs(MH_url,"html.parser")
    print(mh_soup)

    # Retrieval of Mars Hemispheres
    results = mh_soup.find_all("div",class_='item')
    hemisphere_image_urls = []
    for result in results:
        product_dict = {}
        titles = result.find('h3').text
        end_link = result.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup= bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        print(titles)
        print(image_url)
        product_dict['title']= titles
        product_dict['image_url']= image_url
        hemisphere_image_urls.append(product_dict)

    # Close Browser
    browser.quit()

    # Results
    mars_data ={
		'news_title' : news_title,
		'summary': news_p,
        'featured_image': image,
		'fact_table': Facts_HTML,
		'hemisphere_image_urls': hemisphere_image_urls,
        'news_url': news_url,
        'jpl_url': jpl,
        'fact_url': MF_url,
        'hemisphere_url': MH_url,
        }
    collection.insert(mars_data)

    print(mars_data)




