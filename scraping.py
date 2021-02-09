# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser) 
    # Run all scraping functions and store results in dictionary
    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": mars_facts(),
          "last_modified": dt.datetime.now(),
          "hemisphere_image_urls": hemisphere_image_urls(browser)
    }
    # Stop webdriver and return data
    browser.quit()
    return data


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
   
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
    # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere_image_urls(browser):
    
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []
    
    # Optional delay for loading the page
    browser.is_element_present_by_css("div.item", wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    collapsible_results = news_soup.select_one('div.collapsible.results')

    picture_items=collapsible_results.find_all("div", class_="item")

    for item in picture_items:
         
        #create dict.
        hemispheres = {}
        #get title
        title=item.find("h3").get_text()
        #add to dict.
        hemispheres["title"] = title
        #get relative image url
        page_url_relative=item.find("a").get('href')
        #create full url to image page
        page_url_full = f'https://astrogeology.usgs.gov{page_url_relative}'
        #visit image page
        browser.visit(page_url_full)
        browser.is_element_present_by_css("ul li", wait_time=1)
        html = browser.html
        pic_soup = soup(html, 'html.parser')
        #get image url for full .jpg
        img_url=pic_soup.find("a", text ='Sample').get('href')
        img_url
        #add to dict.
        hemispheres["img_url"] = img_url
        hemisphere_image_urls.append(hemispheres)

    return hemisphere_image_urls    


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


