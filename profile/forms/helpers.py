from django import forms
from profile.models import CustomField


def custom_fields(form, prefix=''):
    custom_fields = CustomField.objects.all().order_by('order')
    for custom_field in custom_fields:
        if custom_field.type == 'int':
            form.fields[prefix+custom_field.id] = \
                    forms.IntegerField(label=custom_field.label,
                                       required=custom_field.required,
                                       help_text=custom_field.helper_text)
        elif custom_field.type == 'bool':
            form.fields[prefix+custom_field.id] = \
                    forms.BooleanField(label=custom_field.label,
                                       required=custom_field.required,
                                       help_text=custom_field.helper_text)
        else:
            form.fields[prefix+custom_field.id] = \
                    forms.CharField(label=custom_field.label,
                                    required=custom_field.required,
                                    help_text=custom_field.helper_text)
