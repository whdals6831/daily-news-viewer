from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# Create your views here.
def crawling():
    url = 'https://news.naver.com/'
    html = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(html.text,'html.parser')

    news_section = soup.select('#today_main_news > div.hdline_news > ul > li')

    result = []

    for news in news_section:
        a_tag = news.select_one('div > a')
        news_title = a_tag.get_text().strip()
        news_link = url + a_tag['href']

        news_html = requests.get(news_link, headers={"User-Agent":"Mozilla/5.0"})
        news_soup = BeautifulSoup(news_html.text,'html.parser')
        content = news_soup.select_one('#articleBodyContents')
        img_section = news_soup.select_one('.end_photo_org > img')
        img_link = img_section['src']
        reduce_content = content.get_text().strip()[:50]

        news_data = {
                "title" : news_title,
                "link" : news_link,
                "img" : img_link,
                "content": reduce_content
            }

        result.append(news_data)
        
    return result

def home(request):
    return HttpResponse('되냐?')

def test(request):
    if request.method == 'POST':
        return HttpResponse('POST 성공', status=200)
    else:
        result = crawling()
        return HttpResponse(result, status=200)