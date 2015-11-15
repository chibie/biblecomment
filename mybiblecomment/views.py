from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import login
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import (
    FormMixin, CreateView
)
from mybiblecomment.models import Comment
from accounts.forms import LoginForm

import datetime


class IndexView(FormMixin, TemplateView):
    form_class = LoginForm
    template_name = 'biblecomment/index.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['login_form'] = self.get_form()
        context['latest_comments'] = Comment.objects.order_by('-pub_date')
        context['trending_comments'] = Comment.objects.filter(
            pub_date__gte=timezone.now()-datetime.timedelta(weeks=1)).order_by('-was_blessed', '-pub_date')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            login(request, form.get_user())
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class WriteCommentView(CreateView):
    model = Comment
    fields = ['author', 'bible_verse', 'text']
    template_name = 'biblecomment/write_comment.html'
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(WriteCommentView, self).dispatch(self, request, *args, **kwargs)
    """