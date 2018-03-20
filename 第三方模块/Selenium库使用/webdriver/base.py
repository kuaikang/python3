from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

option = webdriver.ChromeOptions()
option.add_argument('disable-infobars') # 不限制受到自动化控制
browser = webdriver.Chrome(chrome_options=option)
try:
    browser.get('http://www.baidu.com')
    # widget_playcount = brower.find_element_by_id("widget-playcount")
    # print(widget_playcount.text)
    # print(brower.current_url)

finally:
    browser.close()
# chromedriver.exe放在python的Scripts目录下