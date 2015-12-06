from django.conf.urls import url
from mybiblecomment.views import *

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^index/', IndexView.as_view(), name="index"),
    url(r'^write/', WriteCommentView.as_view(), name="write-comment"),
    url(r'^comments/', CommentListView.as_view(), name="comment-list"),
    url(r'^comment/(?P<pk>[0-9]+)/', CommentDetailView.as_view(), name="comment-detail"),
]
