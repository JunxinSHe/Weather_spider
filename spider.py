import requests
from bs4 import BeautifulSoup
# pyecharts不同版本效果不同
from pyecharts import Bar

ALL_DATA = []

def parse_page(url):
    headers= {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'Referer':'http://www.weather.com.cn/textFC/hb.shtml'
    }
    response = requests.get(url, headers= headers)
    text = response.content.decode('utf=8')
    soup = BeautifulSoup(text,'html5lib')
    conMidTab = soup.find('div', class_='conMidtab')
    tables = conMidTab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):

            tds = tr.find_all('td')
            if index == 0:
                city_td= tds[1]
            else:
                city_td = tds[0]
            city = list(city_td.stripped_strings)[0]
            temp_td = tds[-2]
            min_temp = list(temp_td.stripped_strings)[0]
            ALL_DATA.append({"city": city, "min_temp": int(min_temp)})
            # print({"city": city, "min_temp": min_temp})

def main():

    urls =[
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hz.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml'
    ]

    for url in urls:
        # 港澳台页面table标签不全，因此需要用html5lib解析器而非lxml
        parse_page(url)

    #分析数据，根据最低气温进行排序
    ALL_DATA.sort(key=lambda data: data['min_temp'])



    #取前10个数据
    data = ALL_DATA[0:10]

    cities = list(map(lambda x:x['city'], data))
    temps = list(map(lambda x:x['min_temp'],data))
    #pyecharts是绘图库
    chart = Bar("最低气温排行")
    chart.add('',cities,temps)
    chart.render('temperature.html')

if __name__ == '__main__':
    main()
