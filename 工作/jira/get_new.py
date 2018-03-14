from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import time
from 工作.jira import send_message

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

if __name__ == '__main__':

    browser.get("http://192.168.121.155:8080")
    time.sleep(2)
    user = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#login-form-username")))
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
        while True:
            time.sleep(60)
            browser.refresh()
            soup = BeautifulSoup(browser.page_source, "lxml")
            lis_new = soup.find(attrs={"class": "list-content"}).select("li")
            new = lis_new[0]
            if new != first:
                send_message.send_message(new.attrs["data-key"], new.attrs["title"], "1074609185@qq.com")
                send_message.send_message(new.attrs["data-key"], new.attrs["title"], "359405466@qq.com")
                print(new.attrs["data-key"], new.attrs["title"])
                first = new
