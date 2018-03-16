from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import time
from 工作.jira import send_message

browser = webdriver.Chrome()
browser.maximize_window()
wait = WebDriverWait(browser, 30)

if __name__ == '__main__':

    browser.get("http://192.168.121.155:8080")
    time.sleep(1.5)
    user = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#login-form-username")))
    user.send_keys("蒯康")
    browser.find_element(By.CSS_SELECTOR, "#login-form-password").send_keys("111111")
    browser.find_element(By.CSS_SELECTOR, "#login").click()
    time.sleep(0.3)
    browser.get("http://192.168.121.155:8080/projects/EXY/issues")
    # 显示所有问题和筛选器
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#full-issue-navigator > a"))).click()
    sel = browser.find_element(
        By.CSS_SELECTOR,
        "#content > div.navigator-container > div.navigator-body > div > form > div.aui-group > div.aui-item.search-wrap > div.search-container > div.search-options-container > span > a.switcher-item.active"
    )
    # 判断是否是简单
    if sel.text != "简单":
        browser.find_element(By.LINK_TEXT, "高级").click()
    # 清空查询jql
    search = browser.find_element_by_id("advanced-search")
    search.clear()
    jql = "project = EXY AND resolution = Unresolved AND assignee in (单文进, 羊晓颖, currentUser()) "
    jql += "ORDER BY created DESC, priority DESC, updated DESC"
    search.send_keys(jql)
    # 查询
    browser.find_element_by_xpath(
        '//*[@id="content"]/div[1]/div[3]/div/form/div[1]/div[1]/div[1]/div[2]/button').click()
    while True:
        command = input(">>:")
        if command != 'start':
            continue
        soup = BeautifulSoup(browser.page_source, "lxml")
        lis = soup.find(attrs={"class": "list-content"}).select("li")
        first = lis[0]
        while True:
            # 60秒刷新一次
            time.sleep(50)
            browser.find_element_by_xpath(
                '//*[@id="content"]/div[1]/div[3]/div/form/div[1]/div[1]/div[1]/div[2]/button').click()
            time.sleep(10)
            soup = BeautifulSoup(browser.page_source, "lxml")
            # 获取最新
            lis_new = soup.find(attrs={"class": "list-content"}).select("li")
            new = lis_new[0]
            # 判断是新的bug
            if new != first:
                send_message.send_message(new.attrs["data-key"], new.attrs["title"], "359405466@qq.com")
                print(new.attrs["data-key"], new.attrs["title"])
                first = new
