from pypinyin import pinyin, lazy_pinyin
import pypinyin

if __name__ == '__main__':
    
    print(pinyin('蒯康'))

    # 启用多音字模式
    print(pinyin('重重', heteronym=True))

    # 设置拼音风格
    print(pinyin('重重', style=pypinyin.INITIALS))

    # 不考虑多音字的情况
    print(lazy_pinyin('重心'))
