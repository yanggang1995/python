from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from lxml import html

session_requests = requests.session()
login_url = "http://cf.jetlive.net:9090/login.action"
result = session_requests.get(login_url)
tree = html.fromstring(result.text)

result = session_requests.post(login_url,
                               data={
                                   "os_username": "gang.yang",
                                   "os_password": "yg123"
                               }, headers=dict(referer=login_url))

resp = urlopen('http://cf.jetlive.net:9090/display/BZCPDSJPTJF/v+2.36')
soup = BeautifulSoup(resp, 'html.parser')
tagDate = soup.find('ul', class_="t clearfix")
dates = tagDate.h1.string

tagToday = soup.find('p', class_="tem")
try:
    temperatureHigh = tagToday.span.string
except AttributeError as e:
    temperatureHigh = tagToday.find_next('p', class_="tem").span.string

temperatureLow = tagToday.i.string
weather = soup.find('p', class_="wea").string

tagWind = soup.find('p', class_="win")
winL = tagWind.i.string

print('今天是：' + dates)
print('风级：' + winL)
print('最低温度：' + temperatureLow)
print('最高温度：' + temperatureHigh)
print('天气：' + weather)
