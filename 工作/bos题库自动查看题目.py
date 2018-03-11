from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re, time

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
browser.maximize_window()


def login():
    try:
        browser.get("http://boss.jzexueyun.com/#/login")
        time.sleep(1)
        username = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#app > div > form > div.login-right > div:nth-child(3) > div > div > input")))
        username.clear()
        username.send_keys("root")
        password = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#app > div > form > div.login-right > div:nth-child(4) > div > div > input")))
        password.clear()
        password.send_keys("Exueyun20180126")
        browser.find_element(
            By.CSS_SELECTOR,
            "#app > div > form > div.login-right > div:nth-child(5) > div > div > button > span"
        ).click()
        # 等待跳转到首页
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#app > div > div > div.navbar > ul > li.el-menu-item.current > a"))
        )
    except TimeoutException:
        return login()


def teach_study():
    try:
        # 点击教学
        browser.find_element(By.CSS_SELECTOR, "#app > div > div > div.navbar > ul > li:nth-child(5) > a").click()
        time.sleep(2)
        # 题库管理
        # manage = wait.until(EC.presence_of_element_located(
        #     (By.CSS_SELECTOR, "#app > div > form > div.login-right > div:nth-child(3) > div > div > input"), "题库管理"))
        # manage.click()
        manage = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div/ul/div/a[3]/li')
        manage.click()
        time.sleep(25)
        total = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#app > div > div > section > div > div.content > div.tabelLayout-content > div.table-box > div.pagination-container > div > span.el-pagination__total")))
        count = re.sub("\D", "", total.text)
        print("222")
        for i in range(10):
            css = "#app > div > div > section > div > div.content > div.tabelLayout-content > div.table-box > div.el-table.el-table--fit.el-table--border.el-table--enable-row-hover.el-table--enable-row-transition > div.el-table__body-wrapper > table > tbody > tr:nth-child(%s) > td.el-table_1_column_8.is-left > div > button:nth-child(1) > span"%(i+1)
            browser.find_element(By.CSS_SELECTOR, css).click()
            time.sleep(3)
            browser.back()
    except TimeoutException:
        teach_study()


def main():
    login()
    teach_study()


if __name__ == '__main__':
    main()
