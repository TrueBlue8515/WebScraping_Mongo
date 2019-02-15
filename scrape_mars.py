
# coding: utf-8

# In[1]:


import pandas as pd
import pandas as pd
import re
import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup


# In[2]:


# Html of Mars website
martian_news_url = 'https://mars.nasa.gov/news/'
martian_news_html = requests.get(martian_news_url)


# In[3]:


# Parse with BeautifulSoup
martian_soup = BeautifulSoup(martian_news_html.text, 'html.parser')


# In[4]:


# Print body of html
# print(mars_soup.body.prettify())


# In[5]:


# Find article titles
article_titles = martian_soup.find_all('div', class_='content_title')
article_titles


# In[6]:


# Loop to get article titles
for article in article_titles:
    title = article.find('a')
    title_text = title.text
    print(title_text)


# In[7]:


# Find paragraph text
paragraphs = martian_soup.find_all('div', class_='rollover_description')
paragraphs


# In[8]:


# Loop through paragraph texts
for paragraph in paragraphs:
    p_text = paragraph.find('div')
    news_p = p_text.text
    print(news_p)


# In[9]:


# Browser of Mars space images
martian_images_browser = Browser('chrome', headless=False)
nasa_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
martian_images_browser.visit(nasa_url)


# In[10]:


# Parse with BeautifulSoup
martian_images_html = martian_images_browser.html
nasa_soup = BeautifulSoup(martian_images_html, 'html.parser')


# In[11]:


# Print body of html
# print(nasa_soup.body.prettify())


# In[12]:


# Find image link with BeautifulSoup
images = nasa_soup.find_all('div', class_='carousel_items')
images


# In[13]:


# Loop through images
for nasa_image in images:
    image = nasa_image.find('article')
    background_image = image.get('style')
    # print(background_image)
    
    # extract url - match anything after (.)
    re_background_image = re.search("'(.+?)'", background_image)
    # print(re_background_image)
    
    # Convert to string
    search_background_image = re_background_image.group(1)
    # print(search_background_image)
    
    featured_image_url = f'https://www.jpl.nasa/gov{search_background_image}'
    print(featured_image_url)


# In[ ]:


# Weather tweets with splinter
twitter_browser = Browser('chrome', headless=False)
twitter_url = 'https://twitter.com/marswxreport?lang=en'
twitter_browser.visit(twitter_url)


# In[ ]:


# Parse with BeautifulSoup
twitter_html = twitter_browser.html
twitter_soup = BeautifulSoup(twitter_html, 'html.parser')


# In[ ]:


# Print body of html
# print(twitter_soup.body.prettify())


# In[ ]:


# Weather tweets with BeautifulSoup
martian_weather_tweets = twitter_soup.find_all('p', class_='TweetTextSize')
martian_weather_tweets


# In[ ]:


# Tweets that begin with 'Sol' 
weather_text = 'Sol '

for tweet in martian_weather_tweets:
    if weather_text in tweet.text:
        martian_weather = tweet.text
        print(tweet.text)


# In[ ]:


# Url to Mars facts website
martian_facts_url = 'https://space-facts.com/mars/'


# In[ ]:


# Table from url
martian_facts_table = pd.read_html(martian_facts_url)
martian_facts_table


# In[ ]:


# Select table
martian_facts = martian_facts_table[0]

# Switch columns and rows
martian_facts_df = martian_facts.transpose()
martian_facts_df


# In[ ]:


# Rename columns
martian_facts_df.columns = [
    'Equatorial diameter',
    'Polar diameter',
    'Mass',
    'Moons',
    'Orbit distance',
    'Orbit period',
    'Surface temperature',
    'First record',
    'Recorded by'
]

martian_facts_df


# In[ ]:


# Remove first row
clean_martian_facts_df = martian_facts_df.iloc[1:]
clean_martian_facts_df


# In[ ]:


# Print dataframe in html format
martian_facts_html_table = clean_martian_facts_df.to_html()
print(martian_facts_html_table)


# In[ ]:


# Use splinter to get image and title links of each hemisphere
usgs_browser = Browser('chrome', headless=False)
usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
usgs_browser.visit(usgs_url)


# In[ ]:


# Parse with BeautifulSoup
martian_hemispheres_html = usgs_browser.html
martian_hemispheres_soup = BeautifulSoup(martian_hemispheres_html, 'html.parser')


# In[ ]:


# Print body of html
# print(mars_hemispheres_soup.body.prettify())


# In[ ]:


# Hemisphere image link and title
martian_hemispheres = martian_hemispheres_soup.find_all('div', class_='description')
martian_hemispheres


# In[ ]:


# List of dictionaries 
hemisphere_image_urls = []

# Loop 
for image in martian_hemispheres:
    hemisphere_url = image.find('a', class_='itemLink')
    hemisphere = hemisphere_url.get('href')
    hemisphere_link = 'https://astrogeology.usgs.gov' + hemisphere
    print(hemisphere_link)

    # Visit each link that you just found (hemisphere_link)
    usgs_browser.visit(hemisphere_link)
    
    # Create dictionary 
    hemisphere_image_dict = {}
    
    # Parse html again
    martian_hemispheres_html = usgs_browser.html
    martian_hemispheres_soup = BeautifulSoup(martian_hemispheres_html, 'html.parser')
    
    # Get image link
    hemisphere_link = martian_hemispheres_soup.find('a', text='Original').get('href')
    
    # Get title text
    hemisphere_title = martian_hemispheres_soup.find('h2', class_='title').text.replace(' Enhanced', '')
    
    # Append title and image urls of hemisphere to dictionary
    hemisphere_image_dict['title'] = hemisphere_title
    hemisphere_image_dict['img_url'] = hemisphere_link
    
    # Append dictionaries to list
    hemisphere_image_urls.append(hemisphere_image_dict)

print(hemisphere_image_urls)


# In[ ]:


# Convert this jupyter notebook file to a python script called 'scrape_mars.py'
get_ipython().system(' jupyter nbconvert --to script --template basic mission_to_mars.ipynb --output scrape_mars')


# In[ ]:


# Create root/index route to query mongoDB and pass mars data to HTML template to display data
# @app.route('/')
# def index():
    # marsdata = db.marsdata.find_one()
    # return render_template('index.html', marsdata=marsdata)


# In[ ]:


# Create route called /scrape
# @app.route('/scrape')
# def scrape():
    # data = scrape_mars()
    # marsdata = db.marsdata.insert_many(data)
    # db.marsdata.update({}, data, upsert=True)
    # return "Scraping successful!"


# In[ ]:


# if __name__ == '__main__':
    # app.run(debug=True)
    # scrape_mars()

