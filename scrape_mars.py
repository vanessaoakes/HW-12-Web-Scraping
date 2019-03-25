from bs4 import BeautifulSoup
import requests
from splinter import Browser
from bs4 import BeautifulSoup
import time

def scrape():

    output= {}

#NASA news
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_="content_title")

    for result in results:
        try:
            news_title = result.find('a').text
            output["news_title"] = news_title
            break

        except AttributeError as e:
            print(e)

    results = soup.find_all('div', class_="rollover_description_inner")

    for result in results:
        try:
            news_p = result.text
            output["news_p"] = news_p
        
        except AttributeError as e:
            print(e)
 
#JPL Mars Space Images   

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')

    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')
    main_image =  soup.find_all('img',class_='main_image')
    featured_image_url = "https://www.jpl.nasa.gov" + main_image[0]['src']
    output["featured_image_url"] = featured_image_url
    
#Mars Weather    
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_tweet = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_tweet)

    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')
    tweets =  soup.find_all('p',class_='TweetTextSize')
    mars_weather = tweets[0].text
    output["mars_weather"] = mars_weather


#Mars Hemisphere
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_pictures = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_pictures)

    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')

    pictures = soup.find_all('a',class_='itemLink product-item')
    prev_link = ""

    usgs_list = []

    for picture in pictures:
        mars_images_url = "https://astrogeology.usgs.gov" + picture['href']
        if mars_images_url == prev_link:
            continue
        prev_link = mars_images_url
        print(mars_images_url)
        
        browser.visit(mars_images_url)
        
        soup=BeautifulSoup(browser.html, 'html.parser')
        title = soup.find_all('h2', class_ ="title")[0].text
        
        downloads = soup.find_all('div',class_="downloads")[0]
        image_links = downloads.find_all('a')
        image_link = image_links[1]['href']
        print(image_link)
        print(title) 
        
        dict= {"title": title, "img_url": image_link}
        usgs_list.append(dict)

    output["usgs_list"] =usgs_list

    return output



 
    