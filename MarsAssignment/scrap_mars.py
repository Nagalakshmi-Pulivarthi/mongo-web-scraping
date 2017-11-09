
import requests
from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import time

def scrape():

    scrapeData = {}
    executable_path = {'executable_path':'chromedriver.exe'}
    #browser.find_by_name('send').first.click()

    # # Step1 Scraping
    # ## NASA Mars news
    browser = Browser('chrome', **executable_path)
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    #time.sleep(5)
    news_title  = browser.find_by_css('div.content_title').first.find_by_tag('a').text
    news_p = browser.find_by_css('div.article_teaser_body').first.text
    #print(news_title)
    #print(news_p)

    # ## JPL Mars Space Images - Featured Image
    url1="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url1)
    time.sleep(1)
    browser.find_by_css('.primary_media_feature').find_by_css("a.fancybox").first.click()
    time.sleep(2)
    browser.find_by_css('div.fancybox-wrap').find_by_css("a.button").first.click()
    time.sleep(1)
    feature_Image_Url = browser.find_by_css('img.main_image').first['src']
    #print(feature_Image_Url)

    # ## Mars Weather
    url2="https://twitter.com/marswxreport?lang=en"
    browser.visit(url2)
    mars_weather=browser.find_by_css('div.js-tweet-text-container').find_by_css('p.TweetTextSize').first.text
    #print(mars_weather)


    # ## Mars Facts
    url3="https://space-facts.com/mars/"
    r = requests.get(url3)
    bs=BeautifulSoup(r.content, "lxml")
    table = bs.find_all('table')[0] 
    df = pd.read_html(str(table))[0]
    df.columns = ['Description', 'Value']
    df =df.set_index('Description')
    marsFactsHtml = df.to_html()
    
    # ## Mars Hemisphere
    url4="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    links_list=browser.find_by_css('a.product-item')
    links =[]
    for link in links_list:
        links.append(link['href'])
    links

    hemisphere_image_urls = []
    for link in links:
        browser.visit(link)
        time.sleep(1)
        title = browser.find_by_css('h2.title').text
        href =browser.find_link_by_text('Sample').last["href"]
        hemisphere_image_urls.append({'title':title,'img_url':href} )
        #print(browser4.find_by_id('wide-image').first.find_by_tag('a').first["href"])
    hemisphere_image_urls

    browser.quit()
    scrapeData =  { 'news_title':news_title,
                    'news_p':news_p,
                    'mars_weather':mars_weather,
                    'feature_Image_Url': feature_Image_Url,
                    'marsFactsHtml' : marsFactsHtml,
                    'hemisphere_image_urls' :hemisphere_image_urls
                    } 
    return (scrapeData)