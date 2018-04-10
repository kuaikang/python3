from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

if __name__ == '__main__':
    driver = webdriver.Chrome()
    input(">>:")
    driver.get("http://www.jiaoxueyun.cn/res-view!download.do?resource_id=402837e6505b013401505b01f6f000c7")
    input(">>:")
    driver.quit()
