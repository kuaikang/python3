import requests
from urllib.parse import urlencode

if __name__ == '__main__':
    data = {
        "gradeId":"G04",
        "courseId":"K01",
        "versionId":"V02",
        "volumeId":"1296"
    }
    resp = requests.post("http://www.jiaoxueyun.cn/resources-more-inter!getTrees.do?"+urlencode(data))
    print(resp.text)

