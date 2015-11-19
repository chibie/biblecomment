from django.db import models
from django.conf import settings
from bible.models import Book


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    book = models.ForeignKey(Book, related_name='comments')
    chapter = models.PositiveIntegerField(default=1)
    start_verse = models.PositiveIntegerField(default=1)
    end_verse = models.PositiveIntegerField(default=1)
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    was_blessed = models.PositiveIntegerField(default=0)

    @property
    def _get_reference(self):
        # Returns bible verse complete reference
        if self.start_verse > self.end_verse:
            self.end_verse = self.start_verse
        elif self.start_verse == self.end_verse:
            return "{0} {1}:{2}".format(self.book.name, self.chapter, self.start_verse)
        elif self.start_verse < self.end_verse:
            return "{0} {1}:{2}-{3}".format(self.book.name, self.chapter, self.start_verse, self.end_verse)

    @property
    def _get_reference_text(self):
        # Returns the text of the bible reference
        if self.start_verse == self.end_verse:
            return Book.objects.get(name=self.book.name).chapters.get(number=self.chapter)\
                .verses.get(number=self.start_verse)
        elif self.start_verse < self.end_verse:
            return Book.objects.get(name=self.book.name).chapters.get(number=self.chapter)\
                .verses.filter(number__gte=self.start_verse, number__lte=self.end_verse)

    reference = property(_get_reference)
    reference_text = property(_get_reference_text)

    def __str__(self):
        return self.reference


class Reply(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment = models.ForeignKey(Comment, related_name='replies')
    text = models.TextField()
    pub_date = models.DateTimeField('date published')
    was_blessed = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "replies"