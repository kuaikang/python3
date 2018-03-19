from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
import requests



def get_answer(browser,chapter_id,question_id):
    browser.get("http://www.zujuan.com/question/detail-%s.shtml"%question_id)
    answer = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="J_QuestionList"]/li/div/div[3]/div[2]/div/img')))
    answer_url = answer.attrs["src"]
    print(answer_url)
    resp = requests.get(answer_url)
    f = open("../%s/%s.png"%(chapter_id,question_id),mode="wb")
    f.write(resp.content)
    f.close()
    resp.close()
    browser.close()


if __name__ == '__main__':
    get_answer(browser,"1111","4741168")

