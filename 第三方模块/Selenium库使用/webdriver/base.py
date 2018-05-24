from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

option = webdriver.ChromeOptions()
option.add_argument('disable-infobars') # 不限制受到自动化控制
browser = webdriver.Chrome(chrome_options=option)
wait = WebDriverWait(browser, 10)
try:
    browser.get('http://www.baidu.com')
    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#kw"))  # 页面元素在页面中存在
    )
    input.send_keys('美食')
    # widget_playcount = brower.find_element_by_id("widget-playcount")
    # print(widget_playcount.text)
    # print(brower.current_url)
    input(">>:")
finally:
    browser.close()
# chromedriver.exe放在python的Scripts目录下