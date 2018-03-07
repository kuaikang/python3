from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('Cookie')
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("http://www.zujuan.com/question?categories=119480&bookversion=10902&nianji=119480&chid=2&xd=1")
# tree = driver.find_element_by_id("J_Tree")
# print(tree)
print(driver.page_source)
