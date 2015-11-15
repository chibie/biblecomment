from django.db import models
from django.conf import settings


class AllowReply(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    allow_reply = models.BooleanField(True)


class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    was_blessed = models.PositiveIntegerField(default=0)

    def _get_reference(self):
        """Returns bible verse complete reference"""

        if self.end_verse > self.start_verse:
            return "{0} {1}:{2}-{3}"\
                .format(self.book, self.chapter, self.start_verse, self.end_verse)
        else:
            return "{0} {1}:{2}".format(self.book, self.chapter, self.start_verse)

    reference = property(_get_reference)

    def __str__(self):
        return "{0} by {1}".format(self.reference, self.author)


class Reply(models.Model):
    author = models.OneToOneField(settings.AUTH_USER_MODEL)
    comment = models.ForeignKey(Comment)
    text = models.TextField()
    pub_date = models.DateTimeField('date published')
    was_blessed = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "replies"