from django import forms
from  mybiblecomment.models import Comment

class WriteCommentForm(forms.ModelForm):
    book = forms.ModelChoiceField()