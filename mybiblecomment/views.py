from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormMixin

from mybiblecomment.models import Comment
from mybiblecomment.forms import *
from bible.models import Book

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
            request.session['book_index'] = request.POST['book']
            request.session['chapter'] = request.POST['chapter']
            request.session['start_verse'] = request.POST['start_verse']
            request.session['end_verse'] = request.POST['end_verse']
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CommentListView(TemplateView):
    template_name = 'biblecomment/comment_list.html'
    form_class = ScriptureLookupForm

    def get_context_data(self, **kwargs):
        context = super(CommentListView, self).get_context_data(**kwargs)
        book = self.request.session['book']
        book_index = self.request.session['book_index']
        chapter = self.request.session['chapter']
        start_verse = self.request.session['start_verse']
        end_verse = self.request.session['end_verse']

        if int(start_verse) == int(end_verse):
            context['reference'] = "{0} {1}:{2}".format(book, chapter, start_verse)
        elif int(start_verse) < int(end_verse):
            context['reference'] = "{0} {1}:{2}-{3}".format(book, chapter, start_verse, end_verse)

        data = {'book': book_index, 'chapter': chapter, 'start_verse': start_verse, 'end_verse': end_verse}
        context['scripture_lookup_form'] = self.form_class(data, initial=data)
        context['verses'] = Book.objects.get(name=book).chapters.get(number=int(chapter)).verses\
            .filter(number__gte=int(start_verse), number__lte=int(end_verse))
        context['comments'] = \
            Comment.objects.filter(book__name=book, chapter=chapter, start_verse=start_verse, end_verse=end_verse)

        return context


class CommentDetailView(DetailView):
    model = Comment
    reply_form = ReplyCommentForm
    context_object_name = "comment"
    template_name = "biblecomment/comment_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CommentDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['reply_form'] = self.reply_form
        context['replies'] = Comment.objects.get(pk=self.get_object().pk).replies.all()
        return context

    def post(self, request, *args, **kwargs):
        reply_form = self.reply_form(request.POST)

        if reply_form.is_valid():
            if request.user.is_authenticated():
                reply = reply_form.save(commit=False)
                reply.author = request.user
                reply.name = request.user.username
                reply.email = request.user.email
                reply.comment = self.get_object()
                reply.save()
                return redirect(reverse_lazy('biblecomment:comment-detail', kwargs={'pk': self.get_object().pk}))
            else:
                reply = reply_form.save(commit=False)
                reply.author = request.user
                reply.comment = self.get_object()
                reply.save()
                return redirect(reverse_lazy('biblecomment:comment-detail', kwargs={'pk': self.get_object().pk}))
        else:
            return render(
                request,
                self.template_name,
                context={'reply_form': reply_form, 'comment': self.get_object()}
                )


class WriteCommentView(TemplateView):
    reference_form = ScriptureLookupForm
    comment_form = WriteCommentForm
    template_name = 'biblecomment/write_comment.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WriteCommentView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WriteCommentView, self).get_context_data(**kwargs)
        context['reference_form'] = self.reference_form(user=self.request.user)
        context['comment_form'] = self.comment_form

        return context

    def post(self, request, *args, **kwargs):
        reference_form = self.reference_form(request.POST, user=request.user)
        """
        reference_form = self.reference_form(
            user=request.user,
            book_name=self.reference_form.fields['book'].queryset[int(request.POST['book'])-1].name,
            chapter=request.POST['chapter'],
            start_verse=request.POST['start_verse'],
            end_verse=request.POST['end_verse'],
        )
        """
        comment_form = self.comment_form(request.POST)

        if reference_form.is_valid() and comment_form.is_valid():
            post = comment_form.save(commit=False)
            post.author = request.user
            # post.book__name = reference_form.fields['book'].queryset[int(request.POST['book'])-1].name
            post.book = Book.objects.get(number=request.POST['book'])
            post.chapter = request.POST['chapter']
            post.start_verse = request.POST['start_verse']
            post.end_verse = request.POST['end_verse']
            post.save()
            return redirect(reverse_lazy('biblecomment:index'))
        else:
            return render(
                request,
                self.template_name,
                context={'reference_form': reference_form, 'comment_form': comment_form}
                )
