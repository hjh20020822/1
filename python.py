import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import requests
from bs4 import BeautifulSoup
import re

sheet=[['Date','Gold Price ($/oz)','Gold Change(%)','Silver Price($/oz)','Silver Change(%)']]
original_url = "https://www.icbc.com.cn/column/1438058343720960016.html"
driver=webdriver.Edge()
driver.get(original_url)
xpath='/html/body/div/div[3]/div/div[1]/div/div/table/tbody/tr[]/td[2]/span/a'
flag=0
while 1:
    for i in range(1,40,2):
        try:
            temp=[]
            sleep(0.05)
            xp=xpath[:56]
            xp+=str(i)
            xp+=xpath[56:]
            driver.find_element(By.XPATH,xp).click()
            win=driver.window_handles
            driver.switch_to.window(win[1])
            html=requests.get(driver.current_url)
            html.encoding='utf-8'
            soup=BeautifulSoup(html.text,'html.parser')

            date=int(str(soup.title)[49:57])
            temp.append(date)

            price=str(soup.find_all(string=re.compile('价格')))
            # print(price)

            data=re.findall(r"\d+\.\d*", price)
            data=list(map(float,data))
            # print(data)
            for j in range(price.find('黄金'),len(price)):
                if price[j]=='下':
                    data[0]=-data[0]
                    break
                if price[j]=='上':
                    break

            for j in range(price.find('白银'),len(price)):
                if price[j]=='下':
                    data[2]=-data[2]
                    break
                if price[j]=='上':
                    break

            temp.append(data[1])
            temp.append(data[0])
            temp.append(data[3])
            temp.append(data[2])

            print(temp)
            sheet.append(temp)
            driver.close()
            driver.switch_to.window(win[0])
        except:
            flag=1
            break
    if flag:
        break
    driver.find_element(By.LINK_TEXT, '下一页').click()

driver.quit()

exchange_url='https://chl.cn/?usd'
r=requests.get(exchange_url)
r.encoding='utf-8'
soup=BeautifulSoup(r.text,'html.parser')
date1=str(soup.find_all(string=re.compile('年'))[0])
exchange=str(soup.find_all(string=re.compile('美元='))[2])
exchange_dollar=float(exchange[4:10])
exchange_oz_to_g=28.3495231

# for i in sheet:
#     print(i)
sheet1=[['日期','金价(￥/g)','金涨跌幅(%)','银价(￥/g)','银涨跌幅(%)',exchange,date1]]
for i in range(1,len(sheet)):
    temp=[]
    for j in range(len(sheet[i])):
        temp.append(sheet[i][j])
    temp[1]=round(temp[1]*exchange_dollar/exchange_oz_to_g,2)
    temp[3]=round(temp[3]*exchange_dollar/exchange_oz_to_g,2)
    sheet1.append(temp)
# for i in sheet1:
#     print(i)

with open('price.csv','w',encoding='utf-8-sig',newline="") as c:
    t=csv.writer(c)
    for i in range(len(sheet)):
        t.writerow(sheet[i])

with open('价格.csv','w',encoding='utf-8-sig',newline="") as c:
    t=csv.writer(c)
    for i in range(len(sheet1)):
        t.writerow(sheet1[i])