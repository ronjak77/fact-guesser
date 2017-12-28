from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Proposition(models.Model):
    """
    Define fields and default values for Proposition model
    """
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=True, default='')
    truthvalue = models.BooleanField(default=True)
    owner = models.ForeignKey('auth.User', related_name='propositions', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

    """
    On save, set title
    """
    def save(self, *args, **kwargs):
        options = self.title and {'title': self.title} or {}
        super(Proposition, self).save(*args, **kwargs)
        
    """
    Return unicode representation for displaying as a part of a Proposition object
    """
    def __unicode__(self):
        return str(self.title)
    
    """
    Return string representation for displaying as a part of a Proposition object
    """
    def __str__(self):
        return str(self.title)

class Answer(models.Model):
    """
    Define fields and default values for Answer model
    """
    created = models.DateTimeField(auto_now_add=True)
    answer = models.BooleanField(default=True)
    proposition = models.ForeignKey(Proposition, related_name='answers', on_delete=models.CASCADE)

    """
    Return unicode representation for displaying as a part of a Proposition object
    """
    def __unicode__(self):
        return str(self.answer)
    
    """
    Return string representation for displaying as a part of a Proposition object
    """
    def __str__(self):
        return str(self.answer)