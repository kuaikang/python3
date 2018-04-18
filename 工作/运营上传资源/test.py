import requests

# os.path.splitext()函数将路径拆分为文件名+扩展名

if __name__ == '__main__':
    # with open("F:/小白兔.flv",mode="rb") as f:
    #     files = {'file': ["小白兔.flv", f, 'application/octet-stream']}
    #     resp = requests.post(url="http://test.upload.juziwl.cn/cos/upload", files=files)
        # {'status': 200, 'errorMsg': '上传成功',
        #  'content': {'accessUrl': 'http://test.video.juziwl.cn/exue/20180417/de1b461986894b8eb0f8da28a17d55e0.flv',
        #              'fileSize': 1572126, 'fileName': '%E5%B0%8F%E7%99%BD%E5%85%94.flv', 'fileType': 'flv',
        #              'convertUrl': None, 'coverImg': None, 'success': True}, 'timeStamp': 1523931377241}

    req = {
        "currentSubject": "yy",
        "schoolId": "397698131468230656",
        "schoolName": "研发中心小学",
        "bookId": "030003001017100",
        "unitId": "030003001017100001",
        "chapterId": "030003001017100001001",
        "fileList": [
            {
                "fileName": "小白兔.flv",
                "fileType": "flv",
                "filePath": "http://dfs.res.jzexueyun.com/resources/kx/040003001066100/040003001066100001001/%E5%B0%8F%E7%99%BD%E5%85%94.flv",
                "fileSize": 1572126
            }
        ]
    }
    header = {'accessToken': "2b69b43d-d9b9-4757-9999-d997b3ebaa89"}
    result = requests.post(url="http://test.cloudteach.juziwl.cn/cloud/exueResource/uploadResource", json=req, headers=header)
    print(result.json())