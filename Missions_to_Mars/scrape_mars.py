from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    mars_news_data = Mars_News()
    mars_featured_image_data = Mars_Featured_Image()
    mars_facts_data = Mars_Facts()
    mars_hemispheres_data = Mars_Hemispheres()

    mars_dict = {**mars_news_data, **mars_featured_image_data, **mars_facts_data, **mars_hemispheres_data}

    return mars_dict

def Mars_News():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ## URL of page to be scraped
    # Visit URL
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Retrieve all elements that contain title and paragraph text information
    results = soup.find_all('div', class_='list_text')

    # Get the latest News Title on the Mars News Site
    news_title =results[0].find('div', class_='content_title').text

    # Get the latest Paragraph Text on the Mars News Site
    news_p = results[0].find('div', class_='article_teaser_body').text

    # Store data in a dictionary
    mars_news_data = {
        "news_title": news_title,
        "news_paragraph": news_p
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_news_data


def Mars_Featured_Image():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ## URL of page to be scraped
    # Visit URL
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Click the 'FULL IMAGE' button on each page
    browser.links.find_by_partial_text('FULL IMAGE').click()

    # Get the image url for the current Featured Mars Image
    featured_image = soup.find('img', class_='headerimage fade-in')['src']
    featured_image_url = url2 + featured_image

    # Store data in a dictionary
    mars_featured_image_data = {
        "mars_featured_image_url": featured_image_url}

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_featured_image_data

def Mars_Facts():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ## URL of page to be scraped
    # Visit URL
    url3 = 'https://galaxyfacts-mars.com/'
    browser.visit(url3)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Use Panda's `read_html` to parse the url
    tables = pd.read_html(url3)

    # Find the table containing facts about the Mars including Diameter, Mass, etc.
    # Assign the columns `['Description', 'Value']`
    mars_df = tables[1]
    mars_df.columns = ['Description', 'Value']

    #data cleaning, drop index column
    mars_df = mars_df.set_index('Description')

    html_mars_table=mars_df.to_html()

    # Store data in a dictionary
    mars_facts_data = {"html_mars_table": html_mars_table}

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_facts_data

def Mars_Hemispheres():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ## URL of page to be scraped
    # Visit URL
    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Retrieve items that contain mars hemispheres info
    items = soup.find_all('div', class_='item')

    # Get the latest News Title on the Mars News Site
    hemisphere_image_urls=[]

# Create for loop 
    for item in items:
        image = item.find('a', class_='itemLink product-item')['href']
        browser.visit(url4+image)
    
        image_title=item.find('h3').text
    
        updated_html = browser.html
        updated_soup = bs(updated_html, 'html.parser')
    
        downloads = updated_soup.find('div', class_='downloads')
        full_resolution_image_url=url4+ downloads.find_all('li')[0].a['href']
    
        hemisphere_image_urls.append({"title": image_title, "img_url": full_resolution_image_url})

    # Store data in a dictionary
    mars_hemispheres_data = {"hemisphere_image_urls": hemisphere_image_urls}

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_hemispheres_data