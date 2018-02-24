"""爬取猫眼电影Top100"""
import requests,re
# 获取页面内容
def get_page_index(offset=0):
    try:
        resp = requests.get("http://maoyan.com/board/4?offset="+str(offset))
        if resp.status_code == 200:
            return resp.text
        return None
    except Exception:
        return None
# 对页面内容进行过滤
def parse_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?<a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i><.*?fraction">(.*?)</i>.*?</dd>',re.S)
    data = re.findall(pattern,html)
    for index in data:
        yield {
            'index':index[0],
            # 'img':index[1],
            'title':index[2],
            'actor':index[3].lstrip().rstrip(),
            'time':index[4],
            'score':index[5]+index[6]
        }
    return  data
def main(offset):
    html = get_page_index(offset)
    data = parse_page(html)
    for line in data:
        print(line)

if __name__ == '__main__':
    for i in range(10):
        main(i*10)