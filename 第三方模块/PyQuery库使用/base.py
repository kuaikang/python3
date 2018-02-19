import pyquery
html="""
<div name="mydiv">
    <ul>
        <li id="myli" class="item1 active">first item</li>
        <li class="item2">second item</li>
        <li class="item3">third item</li>
        <li class="item4">fourth item</li>
    </ul>
</div>
"""
from pyquery import PyQuery
doc = PyQuery(html) # 字符串初始化
# doc = PyQuery(url="http://www.baidu.com") # URL初始化
# doc = PyQuery(filename="demo.html") # 文件初始化
doc("#mydiv .item1 li")
doc("ul").find("li") # 查找子元素

print(doc("ul").children(".item1"))
print(doc("li").parent())
print(doc("ul").parents())
doc("ul").siblings("item1.active")

# 遍历
# for li in doc("li").items():
#     print(li)
#     print(li.attr("class")) # 获取属性
#     print(li.text()) # 获取标签内容
#     print(li.html()) # 获取标签内所有html代码

# DOM操作
print("-----------------------")
doc("#myli").remove_class("active")
print(doc("#myli"))
doc("#myli").add_class("active")
print(doc("#myli"))
doc("#myli").attr("name","link") # 没有则添加,有就修改
print(doc("#myli"))
doc("#myli").css("font-size","14px")
print(doc("#myli"))
doc("#myli").remove() # 删除
print(doc("#myli"))