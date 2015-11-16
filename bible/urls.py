from django.conf.urls import url
from bible.views import *

urlpatterns = [
    url(r'^$', book_index, name="index"),
    url(r'^book/(?P<book_slug>([1-3]-)?[a-z]+)/(?P<chapter>[0-9]+)', chapter_detail, name="chapter-detail"),
    url(r'^book/(?P<slug>([1-3]-)?[a-z]+)', book_detail, name="book-detail"),
]
