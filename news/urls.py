from django.urls import path
from django.conf.urls import url
from news.views import scrape, news_list, contacts, about
urlpatterns = [
  path('scrape/', scrape, name="scrape"),
  path('', news_list, name="home"),
  path('contacts/', contacts, name="contacts"),
  url(r'^about/', about, name="about"),
]