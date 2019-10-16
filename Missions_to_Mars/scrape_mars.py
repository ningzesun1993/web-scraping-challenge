
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

#use splinter to scrape the website
def scrape():
    # connect the path from chromedriver
    execute_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **execute_path, headless=False)
    # connect the nasa website to get the title and paragraphs
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)
    # sleep 1s to let chrome load the whole website
    time.sleep(1)
    html = browser.html
    # use beautiful soup to load the website
    soup = bs(html, 'html.parser')
    # scrape the data
    first_bs = soup.find('div', class_='content_title')
    first_title = first_bs.get_text()
    first_para = soup.find('div', class_='article_teaser_body').get_text()
    # get the image
    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_image)
    time.sleep(1)
    soup = bs(browser.html, 'html.parser')
    image = soup.find('img', class_='thumb')['src']
    str_image = 'https://www.jpl.nasa.gov/' + image
    # get the weather
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    time.sleep(1)
    soup = bs(browser.html, 'html.parser')
    weather = soup.find('div', class_='js-tweet-text-container').get_text().replace('\n', '')
    # get mars factors
    url_factor = 'https://space-facts.com/mars/'
    df_factor = pd.read_html(url_factor)
    df_table = df_factor[1]
    df_table = df_table.rename(columns={0: 'description', 1: 'value'})
    df_table = df_table.set_index('description')
    table_str = df_table.to_html()
    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # get hemisphere image
    browser.visit(url_hemi)
    time.sleep(1)
    soup = bs(browser.html, 'html.parser')
    div_img = soup.find_all('div', class_='description')
    hemisphere_image_urls = []
    init_url = 'https://astrogeology.usgs.gov/'
    for i in div_img:
        temp = {}
        temp['title'] = i.a.get_text()
        url_temp = init_url + i.a.get('href')
        browser.visit(url_temp)
        time.sleep(1)
        soup_temp = bs(browser.html, 'html.parser')
        temp['img_url'] = soup_temp.find('a', target='_blank').get('href')
        hemisphere_image_urls.append(temp)
    result = {'news_title': first_title, 'news_p': first_para, 'featured_image_url': str_image,
              'mars_weather': weather, 'mars_facts': table_str, 'hemisphere_image_urls': hemisphere_image_urls}
    browser.quit()
    return result

if __name__ == '__main__':
    print(scrape())


