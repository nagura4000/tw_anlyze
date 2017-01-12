#encoding:utf-8
from selenium import webdriver
import time
import pandas as pd
import datetime


search_word = "検索キーワード"
login_id = "ユーザID"
login_password = "パスワード"

driver = webdriver.Chrome(executable_path='C:\dev\chromedriver_win32\chromedriver.exe')
# TwitterのHP
driver.get('https://twitter.com/login')
screen_name = driver.find_element_by_class_name("js-username-field")
password = driver.find_element_by_class_name("js-password-field")
screen_name.send_keys(login_id)
password.send_keys(login_password)
# ログイン
password.submit()

time.sleep(2)

keyword = driver.find_element_by_class_name("search-input")
#keyword.send_keys("キラキラ橘")
keyword.send_keys(search_word)
searchbtn = driver.find_element_by_xpath("//span[@class='search-icon js-search-action']/button")
# 検索実行
searchbtn.submit()
# 2秒待つ
time.sleep(2)

for i in range(100):
    # スクロールでツイート読み込み
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

tweets = []
for em in driver.find_elements_by_xpath("//div[@class='js-tweet-text-container']"):
    tweets.append(str(em.text).replace('\n',' '))

names = []
for em in driver.find_elements_by_xpath("//strong[@class='fullname js-action-profile-name show-popup-with-id']"):
    names.append(str(em.text).replace('\n',' '))

userids = []
for em in driver.find_elements_by_xpath("//a[@class='account-group js-account-group js-action-profile js-user-profile-link js-nav']"):
    userids.append(em.get_attribute("data-user-id"))

unames = []
for em in driver.find_elements_by_xpath("//span[@class='username js-action-profile-name']/b"):
    unames.append(em.text)

regdates = []
for em in driver.find_elements_by_xpath("//div[@class='content']/div/small[@class='time']/a/span[1]"):
    regtime = datetime.datetime.fromtimestamp(int(em.get_attribute("data-time")))
    regdates.append(regtime)

retweetes = []
for em in driver.find_elements_by_xpath("//button[@class='ProfileTweet-actionButton  js-actionButton js-actionRetweet']"):
    retweetes.append(str(em.text).replace('\n','').replace("リツイート", ''))


resultdf = pd.DataFrame({"date":regdates, "uname":unames, "user_id":userids,
                         "name":names, "retweet":retweetes,  "tweedt":tweets},
                        columns=["date", "uname", "user_id", "name", "retweet", "tweedt"])
# ツイート日時で並び替え
resultdf.sort_index(by='date')

# TSVファイルに出力
resultdf.to_csv("c:\\tmp\\tw.tsv", "\t", index=False)
