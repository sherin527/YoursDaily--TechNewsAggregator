
# Create your views here.
import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline
from time import sleep

requests.packages.urllib3.disable_warnings()

def about(request):
  return render(request, "news/about.html")

def contacts(request):
  return render(request, "news/contacts.html")

def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        'object_list': headlines,
    }
    return render(request, "news/home.html", context)
    
def scrape(request):
  Headline.objects.all().delete()
   
  session = requests.Session()
  session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}

  url = "https://www.freecodecamp.org/news/"
  content = session.get(url, verify=False).content
  soup = BSoup(content, "html.parser")
  News = soup.find_all('article', {"class":"post-card"})
  for artcile in News:
    main = artcile.find_all('a')[0]
    link = "https://www.freecodecamp.org"+main['href']
    image_src = str(main.find('img')['src'])
    if not "http" in image_src:
      image_src = "https://www.freecodecamp.org"+str(main.find('img')['src'])
    title = str(main.find('img')['alt'])
    new_headline = Headline()
    new_headline.title = title
    new_headline.url = link
    new_headline.image = image_src
    new_headline.save()

  url2 = "https://www.entrepreneur.com/topic/coders"
  content = session.get(url2, verify=False).content
  soup = BSoup(content, "html.parser")
  News = soup.find_all('div',{"class":"hero"}) 
  for artcile in News:
    main = artcile.find_all('a')[0]
    link = "https://www.entrepreneur.com"+main['href']
    image_ = str(main.find('img')['src'])
    image_ = image_.replace('&blur=50','')
    title = str(main.find('img')['alt'])
    new_headline = Headline()
    new_headline.title = title
    new_headline.url = link
    new_headline.image = image_
    new_headline.save()

  return redirect("../")

  