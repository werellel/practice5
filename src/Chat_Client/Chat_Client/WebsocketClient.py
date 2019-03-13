
import sys
import requests
import asyncio
import urllib.parse
from websocket import create_connection
import http.client
import json
import time
import string
from bs4 import BeautifulSoup 
import requests 
import re 
import sys 
import pprint

# 댓글을 달 빈 리스트를 생성합니다.
List=[]  
FinalList = []

def print_url(r, *args, **kwargs):
    print(r.url)

def flatten(l): 
    flatList = [] 
    for elem in l: 
        # if an element of a list is a list 
        # iterate over this list and add elements to flatList  
        if type(elem) == list: 
            for e in elem: 
                flatList.append(e) 
        else: 
            flatList.append(elem) 
    return flatList

# 네이버 뉴스 url을 입력합니다.
for i in range(50):
    numberPage = 10079144
    numberPage += i
    url="https://news.naver.com/main/hotissue/read.nhn?mid=hot&sid1=100&cid=1079165&iid=2780573&oid=001&aid=00%d" % numberPage
    print(url)
    oid=url.split("oid=")[1].split("&")[0] 
    aid=url.split("aid=")[1] 
    page=1     
    header = { 
        "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36", 
        "referer":url, 
         
    }  
    while True : 
        c_url="https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=default_society&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news"+oid+"%2C"+aid+"&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page="+str(page)+"&refresh=false&sort=FAVORITE"  
    # 파싱하는 단계입니다.
        r=requests.get(c_url,headers=header) 
        cont=BeautifulSoup(r.content,"html.parser")     
        total_comm=str(cont).split('comment":')[1].split(",")[0] 
       
        match=re.findall('"contents":([^\*]*),"userIdNo"', str(cont)) 
    # 댓글을 리스트에 중첩합니다.
        List.append(match) 
    # 한번에 댓글이 20개씩 보이기 때문에 한 페이지씩 몽땅 댓글을 긁어 옵니다.
        if int(total_comm) <= ((page) * 20): 
            break 
        else :  
            page+=1

        # 리스트 결과입니다.
        flatListResult = flatten(List)
        # print(flatListResult)
        FinalList.extend(flatListResult)
        
    for v in range(50):
        if not FinalList:
            	print("Empty List")
        else:
            modulo = v % 51    
            userID = 'user_%d'% modulo
            if modulo & 1:
                idNumber = 1 
                idNumber += modulo
                receiveID = 'user_%d'% idNumber
                URL = 'http://127.0.0.1:8000/accounts/login/' 
                URLL = 'http://127.0.0.1:8000/messages/%s/' % receiveID
            else:
                idNumber = modulo 
                idNumber -= 1
                receiveID = 'user_%d'% idNumber
                URL = 'http://127.0.0.1:8000/accounts/login/'
                URLL = 'http://127.0.0.1:8000/messages/%s/' % receiveID
            
            client = requests.session()
            # Retrieve the CSRF token first
            print(URL)
            client.get(URL)  # sets cookie
            if 'csrftoken' in client.cookies:
                # Django 1.6 and up
                csrftoken = client.cookies['csrftoken']
            else:
                print("csrf오류 발생")
                csrftoken = client.cookies['csrf']
            login_data = dict(username=userID, password='leanbody', csrfmiddlewaretoken=csrftoken, next='/')
            r = client.post(URL, data=login_data, headers=dict(Referer=URL))
            s = client.get(URLL)
            print(userID, "userID")
            print(receiveID, "receiveID")
            if 'csrftoken' in client.cookies:
                # Django 1.6 and up
                csrftoken = client.cookies['csrftoken']
            else:
                # older versions
                csrftoken = client.cookies['csrf']
            if not FinalList:
                chat_data = dict(username = userID, message ="hogeunryu", csrfmiddlewaretoken=csrftoken, next='/')
                rr = client.post(URLL, data=chat_data, headers=dict(Referer=URL))
                ss = client.get(URLL)
            else:
                chat_data = dict(username = userID, message =FinalList[0], csrfmiddlewaretoken=csrftoken, next='/')
                rr = client.post(URLL, data=chat_data, headers=dict(Referer=URL))
                ss = client.get(URLL)
                print(FinalList[0],'FinalList[0]')
                del FinalList[0]