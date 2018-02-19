from bs4 import BeautifulSoup
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<div><p name="hello">Hello</p><span>I am span tag</span><input type="text"></div>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
</body>
</html>
"""
soup = BeautifulSoup(html,"lxml")
# print(soup.prettify())
print("title:",soup.title)
print("title-type:",type(soup.title))
print("head:",soup.head)
print("p:",soup.p) # 如果有多个，返回第一个

print(soup.title.name)
print(soup.p.attrs["name"]) # 返回第一个p标签的name属性
print(soup.p["name"]) # 同上
print(soup.title.string) # 获取标签的内容
print(soup.head.title.string) # 嵌套选择

print("*************")
print(soup.body.contents)
print("*************")
for i,child in enumerate(soup.body.children):
    print(i,child) # 打印所有的子节点
print("*************")
for i,child in enumerate(soup.body.descendants):
    print(i,child) # 打印所有的子孙节点
print("-------------")
print(soup.span.parent) # 返回父节点的全部内容
print("--------------------------------------")
print(list(enumerate(soup.span.next_siblings))) # 所有的兄弟节点
print(list(enumerate(soup.span.previous_siblings))) # 前面的兄弟节点