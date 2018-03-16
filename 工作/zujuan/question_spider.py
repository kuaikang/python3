import requests
from urllib.parse import urlencode


def main(categories):
    url = "http://www.zujuan.com/question/list?"
    req = {
        "categories": categories,
        "question_channel_type": "1",
        "difficult_index": "",
        "grade_id[]": "0",
        "page": "1",
        "_": "1521181947726",
        "kid_num": "",
        "exam_type": "",
        "sortField": "time"
    }
    grade7 = {"grade_id[]": "7"}
    grade8 = {"grade_id[]": "8"}
    grade9 = {"grade_id[]": "9"}
    head = {
        "Cookie": "_ga=GA1.2.1209185538.1520329414; _gid=GA1.2.467343208.1521168412; PHPSESSID=s0e19ph7arjla9r077855f03j0; _csrf=5b74e1fd141508c4e6945a640601d130059a37435c17b5902fa1546f7044c22ca%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22quDlFrtJ7ibskH-7KD2fW1S-LbFHbZgR%22%3B%7D; isRemove=1; Hm_lvt_6de0a5b2c05e49d1c850edca0c13051f=1520917709,1521168412,1521170767,1521177189; chid=27e8704a451201531cc9941f6f3b709b7e13397751c04b090603ffdb0a56dfb9a%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22chid%22%3Bi%3A1%3Bs%3A1%3A%222%22%3B%7D; xd=302c76d9e27c6fb0e1f815bdf637ae7f9ec27997dd7c18c9fcf7c68da09ff5c8a%3A2%3A%7Bi%3A0%3Bs%3A2%3A%22xd%22%3Bi%3A1%3Bs%3A1%3A%222%22%3B%7D; Hm_lpvt_6de0a5b2c05e49d1c850edca0c13051f=1521181950"
    }
    params = urlencode(req) + "&" + urlencode(grade7) + "&" + urlencode(grade8) + "&" + urlencode(grade9)
    resp = requests.get(url + params, headers=head)
    resp.close()
    for js in resp.json().get("data"):
        quest = js.get("questions")
        for q in quest:
            print(q.get("question_text"))
            print(q.get("options"))  # 选项
            print(q.get("knowledge"))


if __name__ == '__main__':
    f = open("cz_chapter.txt", mode="r", encoding="utf8")
    for line in f.readlines():
        line = line.split(",")
        main(line[0])
