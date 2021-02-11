import urllib.request, urllib.error
from urllib.parse import quote
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd
from time import sleep

df = pd.read_csv('gaishi.csv', encoding='UTF-8')
csvlist = [["","本社位置","資本金","設立年","従業員数"]]

for i in range(len(df)):

    corporate_name = df.loc[i,'corporate_name']
    print(corporate_name)

    # 以下からBeautiful Soup
    url = 'https://fumadata.com/search?corporate_name=' + quote(str(corporate_name))
    # URLを開く
    user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150"}
    request = urllib.request.Request(url=url, headers=user_agent)
    html = urllib.request.urlopen(request)

    # sleep(2)
    # BeautifulSoupで開く
    soup = BeautifulSoup(html, "html.parser")

    # list型（BeautifulResult型）で格納されている
    tag_mainbox = soup.select(".s_res") #<div>
    print(tag_mainbox)

    try: # データがない場合がある
        if not tag_mainbox == None:
            news_tag_00 = tag_mainbox[5]
            news_tag_01 = tag_mainbox[6].findAll("li")[1] 
            news_tag_02 = tag_mainbox[6].findAll("li")[2] 
            news_tag_03 = tag_mainbox[6].findAll("li")[3] 
        else:
            news_tag_00 = tag_mainbox[2]
            news_tag_01 = tag_mainbox[3].findAll("li")[1] 
            news_tag_02 = tag_mainbox[3].findAll("li")[2] 
            news_tag_03 = tag_mainbox[3].findAll("li")[3] 
            
    except:
        continue
    
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

    csvlist.append([str(corporate_name), txt_list[0], txt_list[1], txt_list[2], txt_list[3]])

    # CSVファイルを開く。ファイルがなければ新規作成する。
    f = open("gaishi_data.csv", "w")
    writecsv = csv.writer(f, lineterminator='\n')
    # 出力
    writecsv.writerows(csvlist)


    '''
    with open('test.csv', 'w') as f:
        for line in map(str.strip, f):
            csv.writer.writerrows(csvlist)
    '''