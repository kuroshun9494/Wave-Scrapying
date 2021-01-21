#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#urllib.requestモジュールをインポート


# In[ ]:


import requests


# In[ ]:


# BeautifulSoupクラスをインポート


# In[ ]:


from bs4 import BeautifulSoup 


# In[ ]:


#URLの文字列を解析するPythonの標準ライブラリ


# In[ ]:


from urllib.parse import urljoin


# In[ ]:


#パスワード非表示


# In[ ]:


#import getpass


# In[ ]:


#日付インポート


# In[ ]:


from datetime import datetime as dt


# In[115]:


import MySQLdb


# In[ ]:


#ログイン処理


# In[ ]:


# メールアドレスとパスワードの指定
USER = "shunta9494shunta@gmail.com"
PASS = "rikujyou94"
#PASS = getpass.getpass('input your password: ')

# セッションを開始
session = requests.session()

# ログイン
login_info = {
    "account":USER,
    "password":PASS,
    #"back":"index.php",
    #"mml_id":"0"
}

# action
url_login = "https://m.bc01.com/login/?s=1&next_url=http%3A%2F%2Fwww.bcm-surfpatrol.com%2F%3Ffresh%3D"
response = session.post(url_login, data=login_info)
response.raise_for_status() # エラーならここで例外を発生させる

#print(response.text)





# In[ ]:


#必要な部分だけ抽出


# In[ ]:


soup = BeautifulSoup(response.text, "html.parser") #parse = 解析する
elements = soup.find_all('p', class_=['text-need-wrap','line1'])
#print(elements)


# In[ ]:


#配列に格納


# In[145]:


wave_info = []

tdatetime = dt.now()                                               #日付取得
tstr = tdatetime.strftime('%Y/%m/%d')
wave_info.append(tstr)                               

for element in elements:
        element_str = element.string                          #string型に置換
        element_str = element_str.replace('\n','')         #改行コードを削除
        element_str = element_str.replace(' ','')           #空白を削除
        wave_info.append(element_str)
#print(wave_info)


# In[ ]:


#全ページをスクレイピング


# In[147]:


list_chibaN_num = [30,28,29,194,195,1034,31,32,33,34,35,36,37,190,26,25,1068,1054]

for chibaN_num in list_chibaN_num:
    url_content = 'https://www.bcm-surfpatrol.com/wave-detail/3/' + str(chibaN_num) + '/'
    response = session.get(url_content)
    response.raise_for_status() # エラーならここで例外を発生させる
    #print(response.text)
    soup = BeautifulSoup(response.text, "html.parser") #parse = 解析する
    elements = soup.find_all('p', class_=['text-need-wrap','line1'])
    wave_info = []
    
    title = soup.find("title")                                             #タイトルから地点取得
    point = title.string
    point = point.replace('-千葉北無料波情報＆波予想・波予報・動画｜波情報サーフィンBCM','')
    point = point.replace('\n','')
    point = point.replace(' ','')
    wave_info.append(point)
    
    tdatetime = dt.now()                                               #日付取得
    tstr = tdatetime.strftime('%Y/%m/%d')
    wave_info.append(tstr)                               

    for element in elements:
        element_str = element.string                          #string型に置換
        element_str = element_str.replace('\n','')         #改行コードを削除
        element_str = element_str.replace(' ','')          #空白を削除
        element_str = element_str.replace('人','')           #'人'を削除
        wave_info.append(element_str)
    
    # 接続する
    conn = MySQLdb.connect(
    user='shunta01',
    passwd='rikujyou',
    host='localhost',
    db='wave_info')


    cur = conn.cursor() # カーソルを取得する
    sql = 'insert into WaveInfo(SurfPoint, CheckDate, Size, BreakCondition, Weather, Wing, Face, Persons) values (%s,%s,%s,%s,%s,%s,%s,%s)'
    cur.execute(sql, wave_info)
    conn.commit()
    cur.close
    conn.close
    #print(wave_info)


# In[148]:





# 
