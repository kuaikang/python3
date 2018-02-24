from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

brower = webdriver.Chrome()
try:
    brower.get('https://www.baidu.com')

    widget_playcount = brower.find_element_by_id("widget-playcount")
    print(widget_playcount.text)
    print(brower.current_url)

finally:
    brower.close()
# chromedriver.exe放在python的Scripts目录下