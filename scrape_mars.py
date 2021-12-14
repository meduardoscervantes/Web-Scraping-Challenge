##################
# Import Modules #
##################
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def scrape_all():
    listing = {
        "mars_news": mars_news(),
        "mars_img": mars_img(),
        "mars_facts": mars_facts(),
        "mars_hems": mars_hems()
    }
    return listing


##################
# NASA Mars News #
##################
def mars_news():
    browser = Browser()
    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find_all('div', class_="content_title")[0].text
    teaser_para = soup.find_all('div', class_="article_teaser_body")[0].text
    browser.quit()
    return {
        "title": titles,
        "para": teaser_para
    }


##########################################
# JPL Mars Space Images - Featured Image #
##########################################
def mars_img():
    browser = Browser()
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    feat_images = soup.find_all('img', class_="headerimage")
    feat_jpg_url = url + feat_images[0].attrs['src']
    browser.quit()
    return {"feat_img_url": feat_jpg_url}


##############
# Mars Facts #
##############
def mars_facts():
    browser = Browser()
    url = "https://galaxyfacts-mars.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    key = [str(x.text).replace(":", "") for x in soup.find('div', class_="sidebar").find_all('th')]
    value = [str(x.text).replace("\t", "") for x in soup.find('div', class_="sidebar").find_all('td')]
    df = pd.DataFrame({
        "Mars Info": key,
        "Mars Values": value
    })
    table_html = df.to_html(index=False)
    browser.quit()
    return {"table_html": table_html}


####################
# Mars Hemispheres #
####################
def mars_hems():
    browser = Browser()
    url = "https://marshemispheres.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('div', class_="item")
    img_hrefs = [
        url + x.find_all('a', class_="itemLink")[0].attrs['href']
        for x in links
    ]  # Create all of the links to find the images
    src_url = []
    src_title = []
    for x in img_hrefs:  # Visit each website and get the data needed
        browser.visit(x)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        src_url.append(url + soup.find_all('li')[0].find_all('a')[0].attrs['href'])
        src_title.append(str(soup.find_all('h2', class_="title")[0].text).replace(" Enhanced", ""))

    hemisphere_image_urls = [  # Create the dictionary array
        dict({"title": src_title[x], "img_url": src_url[x]})
        for x in range(len(src_title))
    ]
    browser.quit()
    return hemisphere_image_urls
