import requests


if __name__ == '__main__':
    head = {
        "Cookie":"sessionid=s:SXzZXs6CWFIy9RAgmxkLVnst.o/9MvT5NtCqV/cDztB7HkMx3qu6o7DKGAO2nxtk/lSg; Hm_lvt_8a2f2a00c5aff9efb919ee7af23b5366=1521619671; _ga=GA1.2.288418647.1521619671; _gat=1; token=SHwR4LSj1TN65gkuEblumjyHTd93zkhZM8iNcG-Kd4QmYdEACXLFJtdGWuIV5ZCH47jhdcFJPSqBLsKTIaCIgq==; Hm_lpvt_8a2f2a00c5aff9efb919ee7af23b5366=1521682199"
    }
    resp = requests.get("https://www.wmzy.com/api/school-score/fo41wj.html",headers=head)
    print(resp.text)