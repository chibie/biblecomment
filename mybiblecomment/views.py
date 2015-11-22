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
from mybiblecomment.forms import ScriptureLookupForm

import datetime


class IndexView(FormMixin, TemplateView):
    form_class = ScriptureLookupForm
    template_name = 'biblecomment/index.html'
    success_url = reverse_lazy('biblecomment:comment-list')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['scripture_lookup_form'] = self.get_form()
        context['latest_comments'] = Comment.objects.order_by('-pub_date')
        context['trending_comments'] = Comment.objects.filter(
            pub_date__gte=timezone.now()-datetime.timedelta(weeks=1)).order_by('-was_blessed', '-pub_date')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            request.session['book'] = form.fields['book'].queryset[int(request.POST['book'])-1].name
            request.session['chapter'] = request.POST['chapter']
            request.session['start_verse'] = request.POST['start_verse']
            request.session['end_verse'] = request.POST['end_verse']
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CommentListView(TemplateView):
    template_name = 'biblecomment/comment_list.html'

    def get_context_data(self, **kwargs):
        context = super(CommentListView, self).get_context_data(**kwargs)
        if int(self.request.session['start_verse']) == int(self.request.session['end_verse']):
            context['reference'] = "{0} {1}:{2}".format(
                self.request.session['book'],
                self.request.session['chapter'],
                self.request.session['start_verse']
            )
        elif int(self.request.session['start_verse']) < int(self.request.session['end_verse']):
            context['reference'] = "{0} {1}:{2}-{3}".format(
                self.request.session['book'],
                self.request.session['chapter'],
                self.request.session['start_verse'],
                self.request.session['end_verse']
            )
        context['comments'] = Comment.objects.filter(
            book__name=self.request.session['book'],
            chapter=self.request.session['chapter'],
            start_verse=self.request.session['start_verse'],
            end_verse=self.request.session['end_verse']
        )
        return context


class WriteCommentView(CreateView):
    model = Comment
    fields = ['author', 'bible_verse', 'text']
    template_name = 'biblecomment/write_comment.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(WriteCommentView, self).dispatch(self, request, *args, **kwargs)
