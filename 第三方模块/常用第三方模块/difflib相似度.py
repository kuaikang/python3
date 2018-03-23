import difflib

if __name__ == '__main__':
    str1 = "长江、黄河的河流概况(发源地、注入海洋、长度、主要支流与湖泊、河段划分、流经地形区、流经省级行政区域单位(简称"
    str2 = "长江、黄河的河流概况(发源地、注入海洋、长度、主要支流与湖泊、河段划分、流经地形区、流经省级行政区域单位(简称)"
    d = difflib.SequenceMatcher(str1, str2)
    print(d.quick_ratio())
    print(d.ratio())
