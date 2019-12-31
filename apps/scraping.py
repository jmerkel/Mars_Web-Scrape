# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

#.find() = Find first class & Attribute
#.find_all() = find ALL tags & attributes
#.get_text() = only retrieve text, no HTML

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path='/usr/local/bin/chromedriver', headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres" : mars_hemispheres(browser),
        "last_modified": dt.datetime.now()
    }
    return data

def picNav(imgURL):
    browser = Browser("chrome", executable_path='/usr/local/bin/chromedriver', headless=True)
    browser.visit(imgURL)

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        #news_p
    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    
    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url


def mars_facts():
    try:
        # Parse first table ([0]) that is found
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    df.columns=['description', 'value']     # Assign column names
    df.set_index('description', inplace=True)     # Specify index as description
    return df.to_html()

# ### Hemispheres
def mars_hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    baseURL = 'https://astrogeology.usgs.gov'

    dictList = []

    browser.visit(url)
    browser.is_element_present_by_css("thumb", wait_time=1)
    thumbnails = browser.find_by_tag('h3')

    for i in range(0,4):
        thumbnails[i].click()

        html = browser.html
        hemisphereSoup = BeautifulSoup(html, 'html.parser')

        # Find the relative image url
        img_url_rel = hemisphereSoup.select_one('.wide-image').get("src")
        hemi_title = hemisphereSoup.find("h2", class_='title').get_text()
        img_url = f'{baseURL}{img_url_rel}'

        #Add to dictionary
        hemisphereDict = {}
        hemisphereDict['img_url'] = img_url
        hemisphereDict['title'] = hemi_title
        dictList.append(hemisphereDict)

        browser.back()
        browser.is_element_present_by_css("thumb", wait_time=1)
        thumbnails = browser.find_by_tag('h3')

    return dictList




if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())