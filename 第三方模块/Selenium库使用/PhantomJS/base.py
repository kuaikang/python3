from selenium import webdriver

driver = webdriver.PhantomJS(executable_path="phantomjs.exe")
driver.get("http://www.zujuan.com/question?chid=2&xd=1")
data = driver.find_element_by_id("J_Tree")
print(data.text)