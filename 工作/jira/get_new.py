from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

if __name__ == '__main__':

    browser.get("http://192.168.121.155:8080")
    user = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#login-form-username")))
    user.send_keys("蒯康")
    browser.find_element(By.CSS_SELECTOR, "#login-form-password").send_keys("111111")
    browser.find_element(By.CSS_SELECTOR, "#login").click()
    while True:
        command = input(">>:")
        if command != 'start':
            continue
        soup = BeautifulSoup(browser.page_source, "lxml")
        lis = soup.find(attrs={"class": "list-content"}).select("li")
        first = lis[0]
        count = 0
        while True:
            count = count + 1
            time.sleep(60)
            browser.refresh()
            print("第%s次刷新" % count)
            soup = BeautifulSoup(browser.page_source, "lxml")
            lis_new = soup.find(attrs={"class": "list-content"}).select("li")
            if lis_new[0] != first:
                print(lis_new[0].attrs["data-key"], lis_new[0].attrs["title"])
                first = lis_new[0]
