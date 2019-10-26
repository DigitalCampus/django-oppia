from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from quiz.models import Question


class Response(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created', default=timezone.now)
    lastupdated_date = models.DateTimeField('date updated', default=timezone.now)
    score = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    title = models.TextField(blank=False)
    order = models.IntegerField(default=1)

    class Meta:
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')

    def __unicode__(self):
        return self.title


class ResponseProps(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    value = models.TextField(blank=True)

    class Meta:
        verbose_name = _('ResponseProp')
        verbose_name_plural = _('ResponseProps')

    def __unicode__(self):
        return self.name