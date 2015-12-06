from django import forms
from bible.models import Book
from mybiblecomment.models import Comment, Reply


class ScriptureLookupForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), empty_label=None, required=True)
    chapter = forms.CharField(
        widget=forms.TextInput(attrs={'maxlength': '3', 'size': '3', 'value': '1'}))
    start_verse = forms.CharField(
        widget=forms.TextInput(attrs={'maxlength': '3', 'size': '3', 'value': '1'}))
    end_verse = forms.CharField(
        widget=forms.TextInput(attrs={'maxlength': '3', 'size': '3', 'value': '1'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user') or None
        super(ScriptureLookupForm, self).__init__(*args, **kwargs)

    def clean_chapter(self):
        cleaned_data = super(ScriptureLookupForm, self).clean()
        book = cleaned_data.get("book")
        chapter = cleaned_data.get("chapter")

        if book and chapter:
            if int(chapter) > len(Book.objects.get(name=book).chapters.all()):
                raise forms.ValidationError(
                    "%(book)s does not have up to %(chapter)s chapters.",
                    params={'book': book, 'chapter': chapter},
                    code='invalid_chapter'
                )
        return chapter

    def clean_start_verse(self):
        cleaned_data = super(ScriptureLookupForm, self).clean()
        book = cleaned_data.get("book")
        chapter = cleaned_data.get("chapter")
        start_verse = cleaned_data.get("start_verse")

        if book and chapter and start_verse:
            if int(start_verse) > len(Book.objects.get(name=book).chapters.get(number=chapter).verses.all()):
                raise forms.ValidationError(
                    "%(book)s %(chapter)s does not have up to %(verse)s verses.",
                    params={'book': book, 'chapter': chapter, 'verse': start_verse},
                    code='invalid_start_verse'
                )
        return start_verse

    def clean_end_verse(self):
        cleaned_data = super(ScriptureLookupForm, self).clean()
        book = cleaned_data.get("book")
        chapter = cleaned_data.get("chapter")
        end_verse = cleaned_data.get("end_verse")

        if book and chapter and end_verse:
            if int(end_verse) > len(Book.objects.get(name=book).chapters.get(number=chapter).verses.all()):
                raise forms.ValidationError(
                    "%(book)s %(chapter)s does not have up to %(verse)s verses.",
                    params={'book': book, 'chapter': chapter, 'verse': end_verse},
                    code='invalid_end_verse'
                )
        return end_verse

    def clean(self):
        cleaned_data = super(ScriptureLookupForm, self).clean()
        book = cleaned_data.get("book")
        chapter = cleaned_data.get("chapter")
        start_verse = cleaned_data.get("start_verse")
        end_verse = cleaned_data.get("end_verse")

        if book and chapter and start_verse and end_verse:
            if int(end_verse) < int(start_verse):
                raise forms.ValidationError(
                    "Did you mean %(book)s %(chapter)s : %(end_verse)s - %(start_verse)s?",
                    params={'book': book, 'chapter': chapter, 'start_verse': start_verse, 'end_verse': end_verse},
                    code='invalid_reference'
                )

            query_reference = Comment.objects.filter(
                author=self.user.username,
                book=book,
                chapter=chapter,
                start_verse__gte=start_verse,
                end_verse__lte=end_verse,
            )

            if len(query_reference) > 0:
                raise forms.ValidationError(
                    "You have already commented on %(book)s %(chapter)s : %(start_verse)s - %(end_verse)s.",
                    params={
                        'book': book,
                        'chapter': chapter,
                        'start_verse': start_verse,
                        'end_verse': end_verse
                    },
                    code='invalid_query'
                )

        return self.cleaned_data


class WriteCommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'write your comment here...'}), required=True)

    class Meta:
        model = Comment
        fields = ['text']


class ReplyCommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}), required=False)
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), required=False)
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'write your reply here...'}), required=True)

    class Meta:
        model = Reply
        fields = ['name', 'email', 'text']