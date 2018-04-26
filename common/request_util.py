def get_pic_type(response):
    """获取返回图片的类型,gif.png.jpeg,参数是请求响应"""
    if not response:
        return None
    return response.headers.get('Content-Type').split('/')[-1]


if __name__ == '__main__':
    pass
