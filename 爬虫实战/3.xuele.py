from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
browser = webdriver.Chrome()
wait = WebDriverWait(browser,20)


def login():
    try:
        browser.get("https://cas.xueleyun.com/cas/login")
        user_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#credential > div.id-rect.input-rect > input")))
        pass_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#credential > div.password-rect.input-rect > input")))
        user_input.send_keys("38812526")
        pass_input.send_keys("xl123456")
        browser.find_element(By.CSS_SELECTOR, "#credential > button").click()
        wait.until(EC.title_contains("我的课件"))
    except TimeoutException:
        return login()

def main():
    login()
    get_subject()


if __name__ == '__main__':
    main()