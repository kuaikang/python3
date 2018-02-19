html="""
<div>
    <div class="first">first</div>
    <div class="second">
        <ul class="myul" id="myul">
            <li class="element">123</li>
            <li class="element">12</li>
            <li class="element">1</li>
        </ul>
    </div>
</div>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html,"lxml")
# print(soup.find_all("ul"))
# print(type(soup.find_all("ul")[0]))
# for ul in soup.find_all("ul"):
#     print(soup.find_all("li"))

# print(soup.find_all(attrs={"id":"myul"}))
# print(soup.find_all(attrs={"class":"myul"}))

print(soup.find_all(text="12")) # 精确查找
print(soup.find(text="12")) # 精确查找

print("find和find_all用法一样,fand返回单个元素,find_all返回多个元素")
print("find_praents()返回所有祖先节点,find_parent()直接返回父节点")
print()
print("css选择器".center(50,"-"))
# print(soup.select(".myul"))
# print(soup.select("#myul"))
for ul in soup.select("ul"):
    print(ul["id"]) # 获取属性
    print(ul.attrs["id"]) # 同上

print("获取内容".center(50,"-"))
for li in soup.select("li"):
    print(li.get_text())
