import csv
import datetime

from django.core.exceptions import FieldDoesNotExist
from django.http import HttpResponse
from django.utils import formats
from django.views import View

from profile.models import CustomField, UserProfileCustomField


class ExportAsCSVMixin(View):
    csv_filename = 'data'
    available_fields = []
    field_labels = {}
    export_filter_form = None
    __csv_fields = None

    # Method to only load CSV fields and inspect class once
    @classmethod
    def load_csv_fields(cls, instance):
        if not cls.__csv_fields:
            cls.__csv_fields = {}
            for field_name in cls.available_fields:
                label = instance.get_field_label(field_name)
                if label:
                    cls.__csv_fields[field_name] = {'label': str(label), 'type': 'base'}

        custom_fields = CustomField.objects.all().order_by('order')
        for field in custom_fields:
            cls.__csv_fields[field.id] = {'label': str(field.label), 'type': field.type}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_csv_fields(self)

    # If None, the field does not exist
    def get_field_label(self, field_name):
        if hasattr(self.model, field_name):
            return self.get_field_label_from_attributes(field_name)
        elif field_name in self.field_labels:
            return self.field_labels[field_name]
        else:
            # We try to find a foreignKey model field
            field_model = field_name.split('__')
            if len(field_model) == 2 and field_model[0] in dir(self.model):
                model = self.model._meta.get_field(field_model[0]).remote_field.model
                return model._meta.get_field(field_model[1]).verbose_name.strip()
        return None

    def get_field_label_from_attributes(self, field_name):
        try:
            label = self.model._meta.get_field(field_name).verbose_name.strip()
            if field_name in self.field_labels:
                return self.field_labels[field_name]
            else:
                return label
        except FieldDoesNotExist:
            # If it is not a field, we try to find a property with that name
            if field_name in dir(self.model) or isinstance(getattr(self.model, field_name), property):
                if field_name in self.field_labels:
                    return self.field_labels[field_name]
        return None

    def export_csv(self, request, object_list, filter_list=None, *args, **kwargs):

        now = datetime.datetime.now()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename="{}_{}.csv'.format(self.csv_filename, now.strftime('%Y%m%d'))

        response.write(u'\ufeff'.encode('utf-8'))
        writer = csv.writer(response, dialect='excel', delimiter=str(','), quotechar=str('"'))

        # If no field was selected, we export all of them
        if filter_list is None or len(filter_list) == 0:
            filter_list = self.available_fields

        final_fields = []
        header_row = []

        for field in filter_list:
            if field in self.__csv_fields:
                header_row.append(self.__csv_fields[field]['label'])
                final_fields.append(field)

        writer.writerow(header_row)
        writer = self.export_csv_write_rows(writer, object_list, final_fields)

        return response

    def export_csv_write_rows(self, writer, object_list, final_fields):
        for elem in object_list:
            results = []
            for field in final_fields:
                if self.__csv_fields[field]['type'] == 'base':
                    value = self.get_field_value(elem, field)
                else:
                    customfield = UserProfileCustomField.objects.filter(key_name=field, user=elem).first()
                    value = customfield.get_value() if customfield else None
                results.append(value)
            writer.writerow(results)
        return writer

    # Method to access a value by field name, traversing the foreign key objects
    def get_field_value(self, instance, field):
        field_path = field.split('__')
        attr = instance
        value = None
        for elem in field_path:
            try:
                attr = getattr(attr, elem)
                if isinstance(attr, list):
                    attr = attr[0]
                value = self.get_repr(attr)
            except AttributeError:
                pass

        value = '' if value is None else value
        if isinstance(value, float) or isinstance(value, int):
            value = formats.localize(value, use_l10n=True)
        else:
            value = str(value).strip() if value else ''
        return value

    def get_repr(self, value):
        if callable(value):
            return '%s' % value()
        return value

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['export_csv_fields'] = self.__csv_fields

        if self.export_filter_form:
            context['export_filter_form'] = self.export_filter_form(self.request.GET)

        return context

    def get_list_to_export(self):
        return self.get_queryset()

    def get(self, request, *args, **kwargs):
        if request.GET.get('export', '') == 'csv':
            if 'o' in request.GET:
                request.GET = request.GET.copy()
                del request.GET['o']
            filter_list = request.GET.getlist('csv_fields[]', None)
            object_list = self.get_list_to_export()

            return self.export_csv(request, object_list, filter_list, *args, **kwargs)

        return super().get(request, *args, **kwargs)
