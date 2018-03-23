from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os, time
import sys

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

if __name__ == '__main__':

    browser.get("http://192.168.121.155:8080")
    time.sleep(2)
    user = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#login-form-username")))
    user.send_keys("蒯康")
    browser.find_element(By.CSS_SELECTOR, "#login-form-password").send_keys("111111")
    browser.find_element(By.CSS_SELECTOR, "#login").click()
    while True:
        command = input(">>:")
        if command == "start":
            soup = BeautifulSoup(browser.page_source, "lxml")
            lis = soup.find(attrs={"class": "list-content"}).select("li")
            file = "e.txt"
            if os.path.exists(file):
                os.remove(file)
            f = open(file, mode="w", encoding="utf8")
            for li in lis:
                print(li.attrs["data-key"])
                print(li.attrs["title"])
                f.write(li.attrs["data-key"] + "," + li.attrs["title"].replace("（", "(").replace("）", ")"))
                f.write("\n")
            f.close()
        if command == "end":
            browser.quit()
            sys.exit(0)  # 正常退出
