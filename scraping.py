#10.3.6 - turn JNB into Py
# Import Splinter and BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
#imported this in 10.3.5
import pandas as pd
# imported in 10.5.3
import datetime as dt


# add function to initialize the browser, create a data dict, and end the webdriver
#and return scraped data. 
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
   
    # set variables for news title and paragraph 
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_pic": hemisphere_scrape(browser)
    }
    # Stop webdriver and return data
    browser.quit()
    return data



##old code
##set up executable path. set up URL. set up splinter
#executable_path = {'executable_path': ChromeDriverManager().install()}
#browser = Browser('chrome', **executable_path, headless=False)






### News Title and Paragraph code

##old code before Flask.

##assign the URL and instruct the browser to visit it.
## Visit the mars nasa news site
#url = 'https://redplanetscience.com'
#browser.visit(url)

## Optional delay for loading the page
#rowser.is_element_present_by_css('div.list_text', wait_time=1)

##set up the HTML parser.
##convert the browser HTML to a soup object and then quit the browser. 
#html = browser.html
#news_soup = soup(html, 'html.parser')

#slide_elem = news_soup.select_one('div.list_text')

##begin the scraping
##chain find to previous variable. look inside this info for specific data. 
#slide_elem.find('div', class_='content_title')

## Use the parent element to find the first `a` tag and save it as `news_title`
##only text returned. 
#news_title = slide_elem.find('div', class_='content_title').get_text()
#news_title

##Use the parent element to find the paragraph text
#news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
#news_p

## New code for flask. Had to: 
# turn old code into function and add an argument to it.
# Use a return function instead of print. 
# Use a try/except for errors. 
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p











### Featured Images 
## old code. 10.3.4

## Visit the space image site URL
#url = 'https://spaceimages-mars.com/'
#browser.visit(url)

## Find and click the full image button
#full_image_elem = browser.find_by_tag('button')[1]
#full_image_elem.click()

## Parse the resulting html with soup
#html = browser.html
#img_soup = soup(html, 'html.parser')

## Find the relative image url
#img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
#img_url_rel

## Use the base URL to create an absolute URL
#img_url = f'https://spaceimages-mars.com/{img_url_rel}'
#img_url

## New code
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url













### Mars Facts

## Old code - 10.3.5

##set up code to scrape mars facts. 
#df = pd.read_html('https://galaxyfacts-mars.com')[0]
#df.columns=['description', 'Mars', 'Earth']
#df.set_index('description', inplace=True)
#df

##turn the table above to HTML ready code
#df.to_html()

##now we need to end the session to tell the computer were done. 
#browser.quit()

## New code
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()









#Function to scrape the hemisphere data (challenge)
def hemisphere_scrape(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    try:

        # 3. Write code to retrieve the image urls and titles for each hemisphere.
        for i in range(4):
            #click the link
            browser.links.find_by_partial_text('Hemisphere')[i].click()
            #parse
            html = browser.html
            hemisphere_soup = soup(html, 'html.parser')
            #scrape the page
            title = hemisphere_soup.find('h2', class_='title').text
            img_url = hemisphere_soup.find('li').a.get('href')
            #create dictionary 
            hemispheres = {}
            hemispheres['title'] = title
            hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
            #add into list and loop
            hemisphere_image_urls.append(hemispheres)
            browser.back()

    except AttributeError:
        return None

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls





# code to tell flask that our script is complete and ready for action. 
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())