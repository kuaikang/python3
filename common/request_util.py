def get_pic_type(response):
    """获取返回图片的类型,gif.png.jpeg,参数是请求响应"""
    if not response:
        return None
    return response.headers.get('Content-Type').split('/')[-1]


headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
}
if __name__ == '__main__':
    pass
