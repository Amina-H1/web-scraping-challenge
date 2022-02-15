from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape(): 
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    #Add the url for the Mars News Site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Create BeautifulSoup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # NASA Mars News
    #collect the latest News Title and Paragraph Text and assign variables
    n_title = soup.find_all('div', class_='content_title')[0].text
    n_paragraph = soup.find_all('div', class_='article_teaser_body')[0].text
    browser.quit()


    # JPL Mars Space Images - Featured Image
    # Setup splinter and add url
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    JPL_url = "https://spaceimages-mars.com/"
    browser.visit(JPL_url)
    # Parse HTML 
    JPL_html = browser.html
    JPL_soup = BeautifulSoup(JPL_html, "html.parser")


    # Scrape to find the url of the featured image
    img_source = JPL_soup.find('img', class_='headerimage fade-in').get('src')
    featured_image_url = JPL_url + img_source
    browser.quit()

    # Mars Facts
    facts_url = "https://galaxyfacts-mars.com/"
    mars_facts = pd.read_html(facts_url)
    facts_df = mars_facts[1]

    #Clean the dataframe
    facts_df.columns=['Variables', 'Mars']
    facts_df.set_index('Variables', inplace=True)
    facts_df

    #Convert the dataframe to HTML tabel string
    facts_html = facts_df.to_html()
    facts_html = facts_html.replace("\n", "")
    


    # Mars Hemispheres
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    Hem_url = "https://marshemispheres.com/"
    browser.visit(Hem_url)
    Hem_html = browser.html
    Hem_soup = BeautifulSoup(Hem_html, "html.parser")


    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Get a list of all of the hemispheres
    hemispheres = Hem_soup.find_all('div', class_='item')

    #create for loop
    for i in hemispheres: 
    # Initliase the dictionary
        hemisphere_dict = {}
    #Title
        titles = i.find('h3').text
        t_link = i.find('a', class_='itemLink')['href']
    #Image
        browser.visit(Hem_url + t_link)
        img_html = browser.html
        img_soup = BeautifulSoup(img_html, 'html.parser')
        image = img_soup.find('div', class_= 'downloads')
        image_url = url + image.find('a')['href']

    # Append the dictionary with the image url string and the hemisphere title to a list
    hemisphere_dict['Title'] = titles
    hemisphere_dict['image_url'] = image_url
    hemisphere_image_urls.append(hemisphere_dict)
    
    hemisphere_image_urls    

    browser.quit()

# Mars 
    mars_data = {
        "News_title": n_title,
        "News_paragraph": n_paragraph,
        "Featured_image_url": featured_image_url,
        "Mars_facts": str(facts_html),
        "Hemisphere_imgs": hemisphere_image_urls
    }

    return mars_data