from django.conf.urls import url
from mybiblecomment.views import *

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^index/', IndexView.as_view(), name="index"),
    url(r'^write/', WriteCommentView.as_view(), name="write_comment")
]
