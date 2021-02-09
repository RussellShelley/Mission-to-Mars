#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[2]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# In[3]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[5]:


slide_elem.find("div", class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# In[ ]:





# ### Featured Images

# In[8]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# In[ ]:





# In[13]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# In[ ]:





# In[ ]:





# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# 

# ## Hemispheres

# In[15]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[16]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Optional delay for loading the page
browser.is_element_present_by_css("div.item", wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')

collapsible_results = news_soup.select_one('div.collapsible.results')

picture_items=collapsible_results.find_all("div", class_="item")

for item in picture_items:
    #loop contains this:
    #create dict.
    hemispheres = {}
    #get title
    title=picture_items[0].find("h3").get_text()
    #add to dict.
    hemispheres["title"] = title
    #get relative image url
    page_url_relative=picture_items[0].find("a").get('href')
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


# In[17]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[18]:


# 5. Quit the browser
browser.quit()


# In[ ]:




