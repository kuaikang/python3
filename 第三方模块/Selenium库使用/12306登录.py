from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

browser = webdriver.Chrome()
wait = WebDriverWait(browser,30)
login_url = "https://kyfw.12306.cn/otn/login/init"
username = "359405466@qq.com"
password = "life0410"

city = {
    "苏州":"%u82CF%u5DDE%2CSZH",
    "合肥":"%u5408%u80A5%2CHFH"
}

def login():
    try:
        browser.get(login_url)
        user_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#username")))
        pass_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#password")))
        user_input.send_keys(username)
        pass_input.send_keys(password)
        # 等待用户输入验证码,点击登录
        wait.until(EC.title_contains("我的12306"))
    except TimeoutException:
        return login()

def go_search():
    try:
        index = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#selectYuding > a")))
        index.click()
    except TimeoutException:
        search(str)

def search(fromStation,toStation,begin_time):
    try:
        start = browser.find_element_by_id("fromStationText")
        start.click()
        start.send_keys(fromStation)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#citem_0"))).click()
        ends = browser.find_element_by_id("toStationText")
        ends.click()
        ends.send_keys(toStation)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#citem_0"))).click()
        query = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#query_ticket")))
        query.click()

        '''使用添加cookie的方式,尚未解决呀!!!'''
        # browser.add_cookie({"name":"_jc_save_fromStation","value":fromStation})
        # browser.add_cookie({"name":"_jc_save_toStation","value":toStation})
        # browser.add_cookie({"name":"_jc_save_fromDate","value":begin_time})
    except TimeoutException:
        search()

def main():
    login()
    go_search()
    search("suzhou","hefei","2018-02-26")

if __name__ == '__main__':
    main()
