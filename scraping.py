from bs4 import BeautifulSoup as bs
from selenium import webdriver

def full_page_soup(uri, scroll_pause_secs=1, early_break=None):
    """Takes a URI as argument -- then loads page, scrolls to bottom of window (assuming limited data and not infinite scroll), 
    before returning the entirety as bs4 html soup. 
    early_break is an optional early stopping condition that will test available source html at each iteration."""
    print(datetime.datetime.now())
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    browser = webdriver.Chrome(options=option)
    browser.get(uri)
    time.sleep(1)
    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")
    scroll_counter = 0
    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(scroll_pause_secs)   
        if scroll_counter % 25 == 0: print(f"{scroll_counter}")
        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print('breaking loop...')
            break
        last_height = new_height
        scroll_counter += 1
        if early_break:
            soup = bs(browser.page_source, 'html.parser')
            if early_break(soup):
                break
    print(datetime.datetime.now())
    soup = bs(browser.page_source, 'html.parser')
    browser.quit()
    return soup