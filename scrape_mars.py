from bs4 import BeautifulSoup
from splinter import Browser
from datetime import datetime
from time import sleep
import pandas as pd

def getLastNew(browser) -> dict:
    browser.visit('https://mars.nasa.gov/news/') 
    #long delay had to be introduced because calling .html too soon would pull incomplete data
    sleep(20)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('li', class_="slide")   
    for result in results:
        vhead = result.find('h3').text
        vtext = result.find('div', class_="article_teaser_body").text
        vdate = result.find('div', class_="list_date").text
        newdict = dict(header=vhead, text=vtext, date=vdate)
        return newdict

def getFeaturedImage(browser) -> str:
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    full_image_btn = browser.find_by_id("full_image")
    full_image_btn.click()
    more_info_btn = browser.links.find_by_partial_text("more info")
    more_info_btn.click() 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_url = soup.select_one("figure.lede a img").get("src")
    return f"https://www.jpl.nasa.gov{img_url}"

def getTwitterWeather(browser) -> str:
    browser.visit('https://twitter.com/marswxreport?lang=en')
    #long delay had to be introduced because calling .html too soon would pull incomplete data
    sleep(20)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")

    for result in results:
        if 'InSight sol' in result.text:
            return result.text

def getFactTable() -> str:
    facts_df = pd.read_html('https://space-facts.com/mars/')[0]
    facts_df.columns=["fact", "value"]
    return facts_df.to_html()

def getHemispheres(browser) -> list:
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars') 
    img_list = []
    alinks = len(browser.find_by_css("a.product-item h3"))
    for link in range(alinks): 
        current = browser.find_by_css("a.product-item h3")[link]
        titlelink = current.text
        current.click()
        piclink = browser.links.find_by_text("Sample").first["href"]  
        browser.back()
        new = dict(title=titlelink, img_url=piclink)
        img_list.append(new)
    return img_list

def scrape() -> dict:  
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    lastNew = getLastNew(browser)
    featured_image = getFeaturedImage(browser)
    weather = getTwitterWeather(browser)
    fact_tbl = getFactTable()
    img_hem = getHemispheres(browser)
    creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new = dict(Last_New=lastNew,Featured_img=featured_image,Weather=weather,Facts=fact_tbl,Hemispheres_img=img_hem, Creation_date=creation_date)
    browser.quit()
    return new
