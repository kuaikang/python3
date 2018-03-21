from selenium import webdriver
import time

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("http://www.educlouds.cn/teacher-in!view.do")
    input(">>:")
    f1 = open("version.txt", mode="a", encoding="utf8")
    f = open("grade_subject.txt", mode="r", encoding="utf8")
    for line in f.readlines():  # 一年级,G04,语文,K01,01
        line = line.split(",")
        driver.find_element_by_id(line[1]).click()
        time.sleep(1.5)
        driver.find_element_by_id(line[3]).click()
        time.sleep(1.5)
        versions = driver.find_element_by_id("versionList").find_elements_by_tag_name("a")
        for version in versions:
            v = [line[0], line[1], line[2], line[3], version.text, version.get_property("id")]
            f1.write(",".join(v))
            f1.write("\n")
    f.close()
    f1.close()
    driver.quit()
