import csv
import pandas as pd
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep

options = Options()
options.binary_location = '/usr/bin/google-chrome'
options.add_argument('--headless')
options.add_argument('--window-size=1280,1024')
options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')

chrome = webdriver.Chrome('./driver/chromedriver', options=options)
# 要素が見つかるまで、最大10秒間待機する
chrome.implicitly_wait(10)

# アクセスしたいURL
url_00 = "https://www.google.co.jp/"

# csvの読み込み、検索ワードの格納
reading_csv_path = "./gaishi/gaishi_url.csv"
corporates = pd.read_csv(reading_csv_path, encoding='UTF-8')
search_keywords = corporates.loc[20:,'公式URL'] # except,break時にスタート地点を書く
# search_keywords = ['https://jp.akris.com'] # test用1企業

# csvの書き込み、検索ワード入力
csvlist_0 = [["","福利厚生","健康経営","リモートワーク","お問い合わせ"]]
writing_csv_path = "./gaishi/gaishi_searched.csv"

'''
with open(writing_csv_path, mode="w", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerows(csvlist_0)
'''

csvlist = [[]]

for i, keyword in enumerate(search_keywords):
    
    stats = []
    print('【イテレーション回数:'+str(i)+'】')
    for k in range(4):

        # 45回程度でGoogleのbot対策で連続アクセス制限がかかる？
        if i % 20 == 0 and i != 0:
            sleep(100)

        # url_00を開く
        chrome.get(url_00)
        # print(chrome.current_url) # 遷移チェック

        # 検索ワード入力
        search_box = chrome.find_element_by_name('q')
        # search_box.click()
        search_word = csvlist_0[0][k+1]
        search_box.send_keys(search_word + " " + "site:" + keyword)

        # 検索実行
        search_box.send_keys(Keys.RETURN)
        # print(chrome.title)

        try:
            if k == 3:
                stat = chrome.current_url
            else:
                stat = chrome.find_element_by_id('result-stats').text
                pos = stat.find('件')
                stat = stat[:pos]
                pos = stat.find('約')
                stat = stat[pos+1:]

            print(stat)
            stats.append(stat)
            # csvlist.append([str(keyword), str(stats)])

        except: # 検索結果がない場合
            # 追加
            # csvlist.append([str(keyword), ""]) # 空入力
            print("except")
            stats.append('')
            # 途中まで記録
            '''
            # 終了
            sys.exit()
            '''

    csvlist.append([str(keyword), str(stats[0]), str(stats[1]),str(stats[2]), str(stats[3])])
    print('リスト追加数:'+str(len(csvlist)-1))
    print('タブ数：'+str(len(chrome.window_handles))) # タブ数3を上限

    with open(writing_csv_path, mode="a", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(csvlist[i])

with open(writing_csv_path, mode="w", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerows(csvlist)

chrome.quit()