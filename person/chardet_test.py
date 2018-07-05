import chardet
import requests

if __name__ == '__main__':
    # 检测编码格式,参数是bytes类型数据
    data = chardet.detect(requests.get("http://www.baidu.com").content)
    print(data)
