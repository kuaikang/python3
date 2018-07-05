import keyword


if __name__ == '__main__':
    s = 'abc%s%s'
    print(s%('ab','c'))
    s1 = 'abc{name}{age}'
    print(s1.format(name='tom',age='jack'))
    print(s1.format_map({"name":"tom","age":18}))
    print("http://test/1.png".rpartition('/'))
