from urllib import request
import requests
import json
import datetime
import sys, traceback

def get_api():
    url = "https://data.ntpc.gov.tw/api/datasets/71CD1490-A2DF-4198-BEF1-318479775E8A/json?page=0&size=10000"
    response = request.urlopen(url)
    data = json.loads(response.read())
    _data = {}
    for d in data:
        _data[d["sno"]] = d
    
    return _data

def notify(text):
    token = "lQVSWjdTejZ83H6ahHnyMslWMKHgzaY2Fl1EiuL3Lha"
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"message": text}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, data = data)
    print(r.status_code)

def generate_text(loc1, loc2, loc3, warning=False):
    if warning:
        return f"\n`WARNING! {loc1['sno']}-{loc1['sna']} below threshold. You need to hurry up!`\
    \n{loc1['sno']}-{loc1['sna']}\
    Availability = {loc1['sbi']}/{loc1['tot']}\
    \n{loc2['sno']}-{loc2['sna']}\
    Availability = {loc2['sbi']}/{loc2['tot']}\
    \n{loc3['sno']}-{loc3['sna']}\
    Availability = {loc3['sbi']}/{loc3['tot']}\
    "
    else:
        return f"\n{loc1['sno']}-{loc1['sna']}\
    Availability = {loc1['sbi']}/{loc1['tot']}\
    \n{loc2['sno']}-{loc2['sna']}\
    Availability = {loc2['sbi']}/{loc2['tot']}\
    \n{loc3['sno']}-{loc3['sna']}\
    Availability = {loc3['sbi']}/{loc3['tot']}\
    "

def save_data(*loc):
    """
    datetime, no, name, available, total
    """
    with open('document.csv','a') as fd:
        for data in loc:
            fd.write(f"{datetime.datetime.now()},{data['sno']},{data['sna']},{data['sbi']},{data['tot']}\n")

if __name__ == "__main__":
    """
    sno(站點代號)、sna(中文場站名稱)、tot(場站總停車格)、sbi(可借車位數)、sarea(中文場站區域)
    mday(資料更新時間)、lat(緯度)、lng(經度)、ar(中文地址)、sareaen(英文場站區域)、snaen(英文場站名稱)
    aren(英文地址)、bemp(可還空位數)、act(場站是否暫停營運)
    
    [Ref] https://data.ntpc.gov.tw/datasets/71CD1490-A2DF-4198-BEF1-318479775E8A

    """
    THRESHOLD = 5
    try:
        data = get_api()
        save_data(data["1256"], data["1329"], data["1700"])

        # when below threshold
        if (datetime.datetime.now() >= datetime.datetime.now().replace(hour=8, minute=0, second=0)) and \
            (datetime.datetime.now() <= datetime.datetime.now().replace(hour=8, minute=5, second=0)) and int(data["1256"]["sbi"]) < THRESHOLD:
            notify(generate_text(data["1256"], data["1329"], data["1700"], warning=True))
        elif (datetime.datetime.now() >= datetime.datetime.now().replace(hour=8, minute=30, second=0)) and \
            (datetime.datetime.now() <= datetime.datetime.now().replace(hour=8, minute=35, second=0)):
            notify(generate_text(data["1256"], data["1329"], data["1700"]))
    except:
        traceback.print_exc(file=sys.stdout)

"""
Note:
1414 - 捷運中原站

1256 - 民德立體停車場
1329 - 德光國光街口
1700 - 德光莒光路口
"""