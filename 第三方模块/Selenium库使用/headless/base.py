from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')  # 不显示浏览器,静默模式
# chrome_options.add_argument('disable-infobars')

if __name__ == '__main__':
    driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=None)
    driver.get("http://www.baidu.com")
    element = driver.find_element_by_id("#id")
    if element:
        element.get_attribute("src")  # 获取元素属性
        element.text  # 获取元素文本
    # driver.maximize_window()  # 浏览器最大化
    # driver.set_window_size(100, 200)  # 宽高
    # driver.refresh()  # 刷新页面
    # driver.close()  # 关闭当前页面
    driver.quit()  # 关闭当前窗口并结束进程
