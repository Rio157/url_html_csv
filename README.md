# url_html_csv
BeautifulSoup、seleniumを用いたurl、textの取得、csvへの書き込み

## 動作環境
- Windows 10
- WSL2
- Ubuntu
- Visual Studio Code

## at_search_html2csv.py
- csvからsearch_keywordsを取得→Google検索→1番初めのヒットURLを取得→.comまたは.jpで終わるように成型→csvに格納
- 企業HPを検索するために作成
- YouTubeやindeedのような検索を除外
- タブ数を増やしすぎて重くならないよう、3になるよう順次削除、新しいタブへ移動の操作を追加
- selenium

## at_search_html2csv_hit.py
- csvからsearch_keywordsを取得→Google検索→ヒット数を取得→数字だけ取得→csvに格納
- site:{URL}でページ内検索
- [,'福利厚生','健康経営','リモートワーク','お問い合わせ']の検索キーワードを順次イテレーション
- selenium
- Google検索のため、recaptchaに引っかかってしまう 40回程度で引っかかる　解除時間不明、5時間以内

## at_url2csv_iterated.py
- fuma.co.jpにアクセス→企業名をurlに変換して検索→textを取得して成型→csvに格納
- 列は、["","本社位置","資本金","設立年","従業員数"]
- beautifulsoup
- fuma.co.jpについては、正しい企業名でなければ検索結果が不安定になる　
- ex.)（株）→株式会社 のように前処理が必要か

## つまづいた点
- recaptchaに気付かずびっくり
- UserAgent認証が必要　chromeだが、versionを合わせること
- WSL2は再起動後、もう一度有効化の処理が必要
- 
