from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from bs4 import BeautifulSoup

def naver_crawling():
    url = 'https://news.naver.com/'
    html = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(html.text,'html.parser')

    news_section = soup.select('#today_main_news > div.hdline_news > ul > li')

    result = {
        "news_data":[]
        }

    for news in news_section:
        a_tag = news.select_one('div > a')
        news_title = a_tag.get_text().strip()
        news_link = url + a_tag['href']

        news_html = requests.get(news_link, headers={"User-Agent":"Mozilla/5.0"})
        news_soup = BeautifulSoup(news_html.text,'html.parser')
        content = news_soup.select_one('#articleBodyContents')
        img_section = news_soup.select_one('.end_photo_org > img')
        
        try:
            img_link = img_section['src']
        except:
            img_link = "No Image"

        reduce_content = content.get_text().strip()[:50]

        news_data = {
                "title" : news_title,
                "link" : news_link,
                "img" : img_link,
                "content": reduce_content
            }
        
        result["news_data"].append(news_data)
        
    return result

def daum_crawling():
    
    url = 'https://news.daum.net/'
    html = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(html.text,'html.parser')

    news_section = soup.select('#cSub > div > ul > li')

    result = {
        "news_data":[]
        }

    for news in news_section:
        a_tag = news.select_one('div > a')
        news_link = a_tag['href']

        news_html = requests.get(news_link, headers={"User-Agent":"Mozilla/5.0"})
        news_soup = BeautifulSoup(news_html.text,'html.parser')
        news_title = news_soup.select_one('.tit_view').get_text().strip()
        content = news_soup.select_one('#harmonyContainer')
        try:
            img_link = news.select_one('div > a > img')['src']
        except:
            img_link = "No Image"

        reduce_content = content.get_text().strip()[:50]

        news_data = {
                "title" : news_title,
                "link" : news_link,
                "img" : img_link,
                "content": reduce_content
            }
        
        result["news_data"].append(news_data)

    return result

def ai_times_crawling():
    
    url = 'http://www.aitimes.com'
    html = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(html.text,'html.parser')

    news_section = soup.select('#skin-14 > div')

    result = {
        "news_data":[]
        }

    for news in news_section:
        a_tag = news.select_one('a')
        news_link = url + a_tag['href']
        news_title = news.select_one('a > span.content.for-middle > strong').get_text().strip()
        content = news.select_one('a > span.content.for-middle > span')
        try:
            img_link = news.select_one('a > span.frame.line.for-middle > em')['style'][21:-1]
        except:
            img_link = "No Image"

        reduce_content = content.get_text().strip()[:50]

        news_data = {
                "title" : news_title,
                "link" : news_link,
                "img" : img_link,
                "content": reduce_content
            }
        
        result["news_data"].append(news_data)

    return result

def home(request):
    return HttpResponse('되냐?')

def naver(request):
    if request.method == 'POST':
        return HttpResponse('POST 성공', status=200)
    else:
        result = naver_crawling()
        return JsonResponse(result, json_dumps_params = {'ensure_ascii': True})

def daum(request):
    if request.method == 'POST':
        return HttpResponse('POST 성공', status=200)
    else:
        result = daum_crawling()
        return JsonResponse(result, json_dumps_params = {'ensure_ascii': True})

def times(request):
    if request.method == 'POST':
        return HttpResponse('POST 성공', status=200)
    else:
        result = ai_times_crawling()
        return JsonResponse(result, json_dumps_params = {'ensure_ascii': True})