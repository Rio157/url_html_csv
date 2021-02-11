import urllib.request, urllib.error
from urllib.parse import quote
from bs4 import BeautifulSoup
import csv
import re

# 以下からBeautiful Soup
url = 'https://fumadata.com/search?corporate_name=' + quote('コニカミノルタジャパン株式会社')
# URLを開く
user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96"}
request = urllib.request.Request(url=url, headers=user_agent)
html = urllib.request.urlopen(request)
# BeautifulSoupで開く
soup = BeautifulSoup(html, "html.parser")

# list型（BeautifulResult型）で格納されている
tag_mainbox = soup.select(".s_res") #<div>
# print(tag_mainbox[6])
news_tag_00 = tag_mainbox[5]
news_tag_01 = tag_mainbox[6].findAll("li")[1] #<li><a></a></li>
news_tag_02 = tag_mainbox[6].findAll("li")[2] #<li><a></a></li>
news_tag_03 = tag_mainbox[6].findAll("li")[3] #<li><a></a></li>
    
# tuple型にまとまっている
news_tags = news_tag_00, news_tag_01, news_tag_02, news_tag_03

# テキストのみ抽出
num = 0
txt_list = []
for news_txt in news_tags:
    news_txt = news_txt.text
    print(news_txt)
    txt_list.append(news_txt)
    num += 1

# テキスト化した値(list型)を1つずつ格納
# 必要箇所だけ抽出
'''データ例）
本店(登記)所在地：東京都港区芝浦1丁目1番1号
資本金：397百万円
設立：1947年10月
従業員数：3,508人
'''
txt_list[0] = txt_list[0][10:]
txt_list[1] = int(re.sub("\\D", "", txt_list[1])) * 1000000
txt_list[2] = txt_list[2][3:7]
txt_list[3] = re.sub("\\D", "", txt_list[3])

csvlist = [["","news_tag_00","news_tag_01","news_tag_02","news_tag_03"]]
csvlist.append(['corporate_name', txt_list[0], txt_list[1], txt_list[2], txt_list[3]])

# CSVファイルを開く。ファイルがなければ新規作成する。
f = open("url2csv_output.csv", "w")
writecsv = csv.writer(f, lineterminator='\n')
# 出力
writecsv.writerows(csvlist)


'''
with open('test.csv', 'w') as f:
    for line in map(str.strip, f):
        csv.writer.writerrows(csvlist)
'''