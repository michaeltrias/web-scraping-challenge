from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome",**executable_path, headless=False)

def scrape_all():

    browser = init_browser()
    news_title, news_paragraph = mars_news(browser)

    #run scraping functions then store in dictionary
    scraped_data = { "news_title" : latest_title,
                    "news_paragraph": news_intro,
                    "featured_image": featured_image(browser),
                    "hemispheres": hesmispheres(browser),
                    "weather": twitter_weather(browser),
                    "facts": mars_facts(),
                    "last_modified": dt.datetime.now()
                    }

    browser.quit()
    return scraped_data


def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    titles=[]
    paragraphs =[]

    #gets latest news title
    results = soup.find_all('div',class_="content_title")

    for result in results:
        titles.append(result.text)
    
    latest_title = titles[1]

    # gets news paragraph
    teaser =  soup.find_all('div',class_="article_teaser_body")


    for intro in teaser:
        paragraphs.append(intro)
    
    news_intro = (paragraphs[0].text)
    return latest_title, news_intro

def jpl_image(browser):
    url2= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    html= browser.html
    soup = bs(html,'html.parser')
    #locates and clicks "full image" button
    image = browser.find_by_id('full_image')
    image.click()

    #find more info, and click into it
    moreinfo = browser.find_link_by_partial_text('more info')
    moreinfo.click()

    img_src = img_soup.select_one('figure.lede a img').get("src")
    featured_image_url = f'https://www.jpl.nasa.gov{img_src}'

    return featured_image_url

def hemispheres(browser):

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)


    hemisphere_url=[]


    # create a loop to click on the links, find the achor, and return the image url
    for i in range(4):
        hemisphere ={}
    
        browser.find_by_css("a.product-item h3")[i].click()
    
        #find sample image anchor and extract href
        sample_elem=browser.find_link_by_text('Sample').first
        hemisphere['img_url']= sample_elem['href']
    
        #get title and append object to list
        hemisphere['title'] = browser.find_by_css("h2.title").text
        hemisphere_url.append(hemisphere)
    
        #navigate backwards
        browser.back()

    return hemisphere