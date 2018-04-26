import Levenshtein
import re


def get_hamming(str1, str2):
    """计算汉明距离。要求str1和str2必须长度一致。是描述两个等长字串之间对应 位置上不同字符的个数。"""
    return Levenshtein.hamming(str1, str2)


# 格式化名称
def valid_name(name):
    reg = re.compile(r'[\\/:*?".<>| 《》◎：0123456789\r\n]+')
    valid = reg.findall(name)
    if valid:
        for v in valid:
            name = name.replace(v, '')
    return name


def get_similarity(str1, str2):
    """得到字符串相似度,返回float类型"""
    return Levenshtein.ratio(str1, str2)


if __name__ == '__main__':
    print(get_similarity("hai我是", "1、我是谁"))
    print(Levenshtein.ratio("走近科学", "走进科学"))
