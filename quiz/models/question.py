import json

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Question(models.Model):
    QUESTION_TYPES = (
        ('multichoice', 'Multiple choice'),
        ('shortanswer', 'Short answer'),
        ('matching', 'Matching'),
        ('numerical', 'Numerical'),
        ('multiselect', 'Multiple select'),
        ('description', 'Information only'),
        ('essay', 'Essay question'),
    )
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField('date created', default=timezone.now)
    lastupdated_date = models.DateTimeField('date updated',
                                            default=timezone.now)
    title = models.TextField(blank=False)
    type = models.CharField(max_length=15,
                            choices=QUESTION_TYPES,
                            default='multichoice')

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __str__(self):
        return self.title

    def get_maxscore(self):
        props = QuestionProps.objects.get(question=self, name='maxscore')
        return float(props.value)

    def get_title(self, lang='en'):
        try:
            titles = json.loads(self.title)
            if lang in titles:
                return titles[lang]
            else:
                for l in titles:
                    return titles[l]
        except json.JSONDecodeError:
            pass
        return self.title


class QuestionProps(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    value = models.TextField(blank=True)

    class Meta:
        verbose_name = _('QuestionProp')
        verbose_name_plural = _('QuestionProps')

    def __str__(self):
        return self.name
