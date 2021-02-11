#参照元:https://www.mahirokazuko.com/entry/2019/08/16/202008

UbuntuにSeleniumをインストールする手順
UbuntuでSeleniumを使えるようにするためには

Chromeをインストール
Chrome Driverをインストール
Seleniumをインストール
と3ステップを踏む必要があります。

ここでは、Ubuntu18.04にこれらをインストールする手順をご紹介します。

1. Chromeをインストール
まずはUbuntuにChromeをインストールします。UbuntuにChromeを入れる方法は何通りかあるのですが、ここでは将来的なChromeのアップデートに備えて sudo apt update でChromeのバージョンを最新化できるように apt を使ったインストール方法を採用します。

まずは、 apt-key をダウンロードします。

wget https://dl.google.com/linux/linux_signing_key.pub
sudo apt-key add linux_signing_key.pub
ここで OK というメッセージが出ればOKです。

次に、 apt のソースリストに追加します。

echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
あとは本体をインストールするだけです。

sudo apt-get update
sudo apt-get install google-chrome-stable
しばらく待つとインストールが完了します。

完了したらバージョンを確認してみましょう。

google-chrome --version
# Google Chrome 76.0.3809.100
Google Chrome 76.0.3809.100がインストールされていることが確認できます。

2. Chrome Driverをインストール
SeleniumでChromeを使うためにはChrome Driverが必要です。 Chrome Driverは、先ほどインストールしたChromeのバージョンに合ったものを使う必要があります。

バージョンの互換性については公式ページをご確認ください。


 

こんな感じでリンクが張られているので、先ほど入れたChromeのバージョンと照らし合わせてみてください。

f:id:twx:20190816195951p:plain

今回はGoogle Chrome 76なので、真ん中のリンクに進みます。

f:id:twx:20190816200111p:plain

次にこんな画面になるので、chromedriver_linux64.zip のアドレスをコピーし、Ubuntu上で以下のコマンドを実行してダウンロードします。

wget [chrome driverのアドレス]
つまり、今回はこのようになります。

wget https://chromedriver.storage.googleapis.com/76.0.3809.68/chromedriver_linux64.zip
ダウンロードできたら unzip で展開します。展開先はパスが通っているディレクトリ（例えば /bin）にしましょう。

unzip chromedriver_linux64.zip
sudo chromedriver /bin/
これで完了です。

念の為、バージョンを確認しておきます。

chromedriver --version
# ChromeDriver 76.0.3809.68
3. Seleniumをインストール
最後に、SeleniumをインストールしてChromeが使えるかどうか試してみます。

ここでは、pipでインストールしpythonから使ってみようと思います。

pip install selenium