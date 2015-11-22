from django import forms
from bible.models import Book


class ScriptureLookupForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), empty_label=None, required=True)
    chapter = forms.CharField(
        widget=forms.TextInput(attrs={'maxlength': '3', 'size': '3', 'value': '1'}))
    start_verse = forms.CharField(
        widget=forms.TextInput(attrs={'maxlength': '3', 'size': '3', 'value': '1'}))
    end_verse = forms.CharField(
        widget=forms.TextInput(attrs={'maxlength': '3', 'size': '3', 'value': '1'}))

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

    def clean_book(self):
        cleaned_data = super(ScriptureLookupForm, self).clean()
        book = cleaned_data.get("book")
        chapter = cleaned_data.get("chapter")
        start_verse = cleaned_data.get("start_verse")
        end_verse = cleaned_data.get("end_verse")

        if book and chapter and start_verse and end_verse:
            if int(end_verse) < int(start_verse):
                raise forms.ValidationError(
                    "Did you mean %(book)s %(chapter)s : %(start_verse)s - %(end_verse)s?",
                    params={'book': book, 'chapter': chapter, 'start_verse': start_verse, 'end_verse': end_verse},
                    code='invalid_reference'
                )
        return book