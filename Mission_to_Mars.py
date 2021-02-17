# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup

# Import Pandas
import pandas as pd


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# Set up the HTML parser:
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# Use the parent element to find the teaser paragraph text
news_p  = slide_elem.find("div", class_='article_teaser_body').get_text()
news_p 


### Featured Images

# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)



# Find and click the full image button 
# The [1] index chained at the end of the first line of code below stipulates hat we want to click on the 2nd button. 
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()



# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')



# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel



# look at our address bar in the webpage and add the first part below
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### Mars Facts


# Create a new df from the HTML table. The readhtml() function returns a list of tables found in the html [0] tells us to pull only the first
df = pd.read_html('http://space-facts.com/mars/')[0]
# Assign columns to the new df for clarity
df.columns=['description', 'value']
# Turn the 'description' column into the index 
# inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
df.set_index('description', inplace=True)
df

# Convert df back to html
df.to_html()


# End the session
browser.quit()