from selenium import webdriver

def search(search_key):
    driver = webdriver.Chrome('./chromedriver')

    driver.get('https://www.naver.com/')

    element = driver.find_element_by_xpath(
        "//*[@id='query']")

    element.send_keys(search_key)

    driver.find_element_by_xpath(
        "//*[@id='search_btn']").click()