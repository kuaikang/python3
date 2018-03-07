from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re,pyquery
from selenium.common.exceptions import TimeoutException
browser = webdriver.Chrome()
# browser.page_source 页面html
wait = WebDriverWait(browser, 10)
def search():
    try:
        browser.get("https://www.taobao.com")
        # 输入框
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q")) # 页面元素在页面中存在
        )
        # 页面元素可点击
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#J_TSearchForm > div.search-button > button")))
        input.send_keys('美食')
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))  # 页面元素在页面中存在
        )
        get_pages()
        return total.text
    except TimeoutException:
        return search()

def next_page(page_num):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))  # 页面元素在页面中存在
        )
        # 页面元素可点击
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
        input.clear() # 清除输入框的内容
        input.send_keys(page_num)
        submit.click()
        # 等待元素内文本变成指定内容
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > ul > li.item.active > span"),str(page_num)))
        get_pages()
    except TimeoutException:
        next_page(page_num)

def get_pages():
    # 等待商品加载完毕
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#mainsrp-itemlist .items .item")))
    html = browser.page_source
    doc = pyquery.PyQuery(html)
    items = doc("#mainsrp-itemlist .items .item").items()
    for item in items:
        product = {
            'img':item.find(".pic .img").attr('src'),
            'price':item.find('.price').text(),
            'title':item.find('.title').text()
        }
        print(product)


def main():
    total = search()
    total = int(re.compile("(\d+)").search(total).group(1))
    for index in range(2,total+1):
        next_page(index)

if __name__ == '__main__':
    main()