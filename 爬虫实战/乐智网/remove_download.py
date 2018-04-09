from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


def remove():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    driver.get("http://www.jiaoxueyun.cn/")
    input(">>:")
    while True:
        driver.refresh()
        my_download = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="id-personal-menu"]/li[4]/a')))
        my_download.click()
        print("F5")
        time.sleep(1)
        for i in range(10):
            try:
                button = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[9]/div[8]/div[2]/table/tbody/tr/td[4]/a/img")))
                button.click()
                time.sleep(0.2)
                sure = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "body > div.dialog-delorder > div.dialog-console > a.console-btn-confirm")))
                sure.click()
                time.sleep(0.3)
            except Exception:
                continue


if __name__ == '__main__':
    remove()
