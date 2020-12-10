from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('되냐?')

def test(request):
    if request.method == 'POST':
        return HttpResponse('POST 성공', status=200)
    else:
        return HttpResponse('GET 접근', status=200)