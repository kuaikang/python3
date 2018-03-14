from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)


def index_page():
    browser.get("http://www.zujuan.com")
    input(">>:")
    number = browser.find_element(By.CSS_SELECTOR,
                                  "#select-form > div.g-container.f-cb > div.g-mn1 > div > div.sort > div.total > b")
    size = (int(number.text) + 10 - 1) // 10
    return size


def next_page(page):
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                          '#select-form > div.g-container.f-cb > div.g-mn1 > div > div.page > div > input[type="text"]')))
        input.clear()
        input.send_keys(page)
        browser.find_element(By.CSS_SELECTOR, "#paper-jump").click()
    except TimeoutException:
        next_page(page)


if __name__ == '__main__':
    total = index_page()
    for i in range(1, total):
        next_page(i)

    browser.close()
