import urllib.request, urllib.error, requests
from bs4 import BeautifulSoup
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
reading_csv_path = './white500/white_500_fumad.csv'
corporates = pd.read_csv(reading_csv_path, encoding='UTF-8')
search_keywords = corporates.loc[200:,'corporate_name'] # except,break時にスタート地点を書く
# search_keywords = ['IHI株式会社'] # test用1企業

# 公式ページリスト
# 列名入力
writing_csv_path = "./white500/searched_list.csv"
'''
csvlist_0 = [["","公式URL",]]
with open("searched_list.csv", mode="w", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerows(csvlist_0)
'''

csvlist = [[]]

for i, keyword in enumerate(search_keywords):
    
    print('【イテレーション回数:'+str(i)+'】')
    
    # 45回程度でGoogleのbot対策で連続アクセス制限がかかる？
    if i % 20 == 0 and i != 0:
        sleep(100)

    if i > 1:
        # 3番目のタブで閉じる
        # webdriver.ActionChains(chrome).key_down(Keys.CONTROL).send_keys("w").perform()
        chrome.close()
        # 2番目のタブに戻る
        chrome.switch_to.window(chrome.window_handles[1])
        # 新しいタブ
        chrome.execute_script("window.open('','_blank');")
        # 3番目のタブに移動
        chrome.switch_to.window(chrome.window_handles[2]) # handlesは0から

    else:
        # 新しいタブ
        chrome.execute_script("window.open('','_blank');")
        # i番目のタブに移動
        chrome.switch_to.window(chrome.window_handles[i])

    # url_00を開く
    chrome.get(url_00)
    # print(chrome.current_url) # 遷移チェック

    # 検索ワード入力
    # user-agent偽装確認 print(chrome.page_source)
    search_box = chrome.find_element_by_name('q')
    # search_words = keyword, "AND", "公式"
    # search_box.click()
    search_box.send_keys(keyword + " " + '"AND"' + " " + "公式" + " " + "-YouTube" + " " + "-Instagram" + " " + "-Facebook" + " " + "-Twitter" + " " + "-indeed" + " " + "-LinkedIn" + " " + "-jst" + " " + "-wiki" + " " + "-amazon")

    # 検索実行
    search_box.send_keys(Keys.RETURN)

    # print(chrome.title)

    # class="g" からタイトルとリンクを抽出
    for _ in range(3): # 最大3回実行
        try:
            # 検索結果1つ目のタイトルとリンクを取得
            # タイトルとリンクはclass="r"に入っている
            class_group = chrome.find_elements_by_class_name("yuRUbf")
            # print(class_group)     # 取得できているか確認
            title = class_group[0].find_element_by_class_name('LC20lb').text        # タイトル(class="LC20lb")
            link = class_group[0].find_element_by_tag_name('a').get_attribute('href') # リンク(aタグのhref)

            print(title)
            print(link)

            # リンクから.comまたは.jp以降を削除
            if '.co.jp' in link:
                pos = link.find('.jp')
                link = link[:pos+len('.jp')]
                
            elif '.com' in link:
                pos = link.find('.com')
                link = link[:pos+len('.com')]
            
            print(link) # 削除できたか確認
            csvlist.append([str(keyword), link])

        except:
            # 追加
            # csvlist.append([str(keyword), ""]) # 空入力
            print("except")
            print('リスト追加数:'+str(len(csvlist)-1))
            print('タブ数：'+str(len(chrome.window_handles))) # タブ数3を上限
            # 途中まで記録
            with open(writing_csv_path, mode="a", encoding="utf-8") as f:
                writer = csv.writer(f, lineterminator="\n")
                writer.writerows(csvlist)
            # 終了
            sys.exit()

        else:
            break
    else:
        break
    print('リスト追加数:'+str(len(csvlist)-1))
    print('タブ数：'+str(len(chrome.window_handles))) # タブ数3を上限

with open(writing_csv_path, mode="a", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerows(csvlist)

chrome.quit()