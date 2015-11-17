from django.db import models
from django.conf import settings


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    was_blessed = models.PositiveIntegerField(default=0)

    def _get_reference(self):
        """Returns bible verse complete reference"""
        return ""

    reference = property(_get_reference)

    def __str__(self):
        return "{0} by {1}".format(self.reference, self.author)


class Reply(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment = models.OneToOneField(Comment)
    text = models.TextField()
    pub_date = models.DateTimeField('date published')
    was_blessed = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "replies"