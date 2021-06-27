import math
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError 
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from PIL import Image

from oppia.models import Course
from quiz.models import Question


class CertificateTemplate(models.Model):
    
    # verify template image dimensions
    def validate_image(image):
        img = Image.open(image.file)
        width, height = img.size
        # check height and width
        valid_image = True
        # portrait
        if height > width:
            ratio = height / width
            if height < 842 or width < 595 \
                    or not math.isclose(1.415, ratio, abs_tol=0.01):
                valid_image = False
        # landscape
        else:  
            ratio = width / height
            if width < 842 or height < 595 \
                    or not math.isclose(1.415, ratio, abs_tol=0.01):
                valid_image = False
            
        if not valid_image:
            raise ValidationError(_(u"Please check the size and dimensions of your uploaded certificate template."))

    VALIDATION_OPTION_NONE = "NONE"
    VALIDATION_OPTION_QRCODE = "QRCODE"
    VALIDATION_OPTION_URL = "URL"
    
    VALIDATION_OPTIONS = (
        (VALIDATION_OPTION_NONE, 'None'),
        (VALIDATION_OPTION_QRCODE, 'QR Code'),
        (VALIDATION_OPTION_URL, 'URL')
    )
    
    DISPLAY_NAME_METHOD_USER_FIRST_LAST = 'USER_FIRST_LAST'
    DISPLAY_NAME_METHOD_REGISTRATION_FIELD = 'REGISTRATION_FIELD'
    DISPLAY_NAME_METHOD_FEEDBACK_RESPONSE = 'FEEDBACK_RESPONSE'
    
    DISPLAY_NAME_METHOD_OPTIONS = (
        (DISPLAY_NAME_METHOD_USER_FIRST_LAST, 'User profile - firstname/lastname'),
        (DISPLAY_NAME_METHOD_REGISTRATION_FIELD, 'Registration form field'),
        (DISPLAY_NAME_METHOD_FEEDBACK_RESPONSE, 'Feedback response')
    )
    
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    image_file = models.ImageField(
        upload_to="certificate/templates",
        validators=[validate_image],
        help_text=_(u"Use a .png image of 842px by 595px (at 72dpi), or use equivalent dimension ratio for higher dpi"))

    include_name = models.BooleanField(default=True)
    include_date = models.BooleanField(default=True)
    include_course_title = models.BooleanField(default=True)
    
    name_x = models.IntegerField(default=0)
    name_y = models.IntegerField(default=0)

    date_x = models.IntegerField(default=0)
    date_y = models.IntegerField(default=0)

    course_title_x = models.IntegerField(default=0)
    course_title_y = models.IntegerField(default=0)

    validation = models.CharField(max_length=10,
                                  choices=VALIDATION_OPTIONS,
                                  default=VALIDATION_OPTION_NONE)
    
    validation_x = models.IntegerField(default=0)
    validation_y = models.IntegerField(default=0)
    
    display_name_method = models.CharField(max_length=50,
                                  choices=DISPLAY_NAME_METHOD_OPTIONS,
                                  default=DISPLAY_NAME_METHOD_USER_FIRST_LAST)

    registration_form_field = models.ForeignKey('profile.CustomField',
                                                on_delete=models.SET_NULL,
                                                blank=True,
                                                default=None,
                                                null=True)

    feedback_field = models.ForeignKey(Question,
                                        on_delete=models.SET_NULL,
                                        blank=True,
                                        default=None,
                                        null=True)
    class Meta:
        verbose_name = _('Certificate Template')
        verbose_name_plural = _('Certificate Templates')

    def __str__(self):
        return self.badge.name + ": " + self.course.get_title()
    
    def display_name(self, user):
        if self.display_name_method == \
                self.DISPLAY_NAME_METHOD_USER_FIRST_LAST:
            return True, user.first_name + " " + user.last_name
    
        if self.display_name_method == \
                self.DISPLAY_NAME_METHOD_REGISTRATION_FIELD:
            from profile.models import UserProfileCustomField
            
            try:
                upcf = UserProfileCustomField.objects.get(
                    key_name = self.registration_form_field, user = user)
                return True, upcf.get_value()
            except UserProfileCustomField.DoesNotExist:
                return False, None
            
        if self.display_name_method == \
                self.DISPLAY_NAME_METHOD_FEEDBACK_RESPONSE:
            from quiz.models import QuizAttemptResponse
            # get the most recent response to this question
            response = QuizAttemptResponse.objects.filter(question=self.feedback_field, quizattempt__user=user).order_by('-quizattempt__submitted_date')
            if response.count() == 0:
                return False, None
            else:
                return True, response.first().text
    
    def clean(self, *args, **kwargs):
        if self.display_name_method == \
                self.DISPLAY_NAME_METHOD_REGISTRATION_FIELD \
                and self.registration_form_field is None:
            raise ValidationError(_(u"Please select a registration form field"))
        if self.display_name_method == \
                self.DISPLAY_NAME_METHOD_FEEDBACK_RESPONSE \
                and self.feedback_field is None:
            raise ValidationError(_(u"Please select a feedback question field"))
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super(CertificateTemplate, self).save(*args, **kwargs)