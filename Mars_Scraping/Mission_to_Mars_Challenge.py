#!/usr/bin/env python
# coding: utf-8

# In[19]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup

# Import Pandas
import pandas as pd


# In[20]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# In[5]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[6]:


# Set up the HTML parser:
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[7]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the teaser paragraph text
news_p  = slide_elem.find("div", class_='article_teaser_body').get_text()
news_p 


# ### JPL Space Images Featured Image

# In[21]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[22]:


# Find and click the full image button 
# The [1] index chained at the end of the first line of code below stipulates hat we want to click on the 2nd button. 
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[13]:


# look at our address bar in the webpage and add the first part below
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### Mars Facts

# In[14]:


# Create a new df from the HTML table. The readhtml() function returns a list of tables found in the html [0] tells us to pull only the first
df = pd.read_html('http://space-facts.com/mars/')[0]
# Assign columns to the new df for clarity
df.columns=['description', 'value']
# Turn the 'description' column into the index 
# inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
df.set_index('description', inplace=True)
df


# In[15]:


df.to_html()


# ### Mars Weather

# In[16]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[17]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[18]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# 

# ### Hemispheres

# In[50]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[ ]:





# In[51]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# First, get a list of all of the hemispheres
ref_link = browser.find_by_css("a.product-item h3")

# Next, loop through those links, click the link, find the sample anchor, return the href
for i in range(len(ref_link)):
    hemisphere = {}
    
    # We have to find the elements on each loop to avoid a stale element exception
    browser.find_by_css("a.product-item h3")[i].click()
    
    # Next, we find the Sample image anchor tag and extract the href
    sample_jpg = browser.links.find_by_text('Sample').first
    hemisphere['img_url'] = sample_jpg['href']
    
    # Get Hemisphere title
    hemisphere['title'] = browser.find_by_css("h2.title").text
    
    # Append hemisphere object to list
    hemisphere_image_urls.append(hemisphere)
    
    # Navigate backwards
    browser.back()


# In[52]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[ ]:


# 5. Quit the browser
browser.quit()

