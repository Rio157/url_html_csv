'''
from selenium.webdriver.chrome.options import Options
# Seleniumをあらゆる環境で起動させるChromeオプション
options = Options()
options.add_argument('--disable-gpu');
options.add_argument('--disable-extensions');
options.add_argument('--proxy-server="direct://"');
options.add_argument('--proxy-bypass-list=*');
options.add_argument('--start-maximized');
# options.add_argument('--headless'); # ※ヘッドレスモードを使用する場合、コメントアウトを外す
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = '/usr/bin/google-chrome'
options.add_argument('--headless')
options.add_argument('--window-size=1280,1024')

# DRIVER_PATH = './driver/chromedriver.exe' # ローカル

chrome = webdriver.Chrome('./driver/chromedriver', options=options)
url_00 = "https://www.google.co.jp" #アクセスURL

key_input = input("検索キーワードは：")
search_keywords = ["カレー", "ラーメン", "チャーハン", "とんかつ", "お好み焼き"]

for i, keyword in enumerate(search_keywords):
    if i > 0:
        # 新しいタブ
        chrome.execute_script("window.open('','_blank');")
        # i番目のタブに移動
        chrome.switch_to.window(chrome.window_handles[i])

    # url_00を開く
    chrome.get(url_00)

    # 検索ワード入力
    search_box = chrome.find_element_by_name("q") # name属性の値を取得
    search_words = key_input, "AND", keyword
    search_box.send_keys(" ".join(search_words))

    # 検索実行
    search_box.send_keys(Keys.RETURN)
    print(chrome.title)

# 先頭のタブに戻る
chrome.switch_to.window(chrome.window_handles[0])




