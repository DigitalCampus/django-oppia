import csv
import datetime

from django.core.exceptions import FieldDoesNotExist
from django.http import HttpResponse
from django_filters.views import FilterView


class ExportAsCSVMixin(FilterView):
    csv_filename = 'data'
    available_fields = []
    field_labels = {}
    __csv_fields = None

    # Method to only load CSV fields and inspect class once
    @classmethod
    def load_csv_fields(cls, instance):
        if not cls.__csv_fields:
            cls.__csv_fields = {}
            for field_name in cls.available_fields:
                label = instance.get_field_label(field_name)
                if label:
                    cls.__csv_fields[field_name] = str(label)

    def __init__(self, *args, **kwargs):
        super(ExportAsCSVMixin, self).__init__(*args, **kwargs)
        self.load_csv_fields(self)

    # If None, the field does not exist
    def get_field_label(self, field_name):
        if hasattr(self.model, field_name):
            try:
                label = self.model._meta.get_field(field_name) \
                    .verbose_name.strip()
                if field_name in self.field_labels:
                    return self.field_labels[field_name]
                else:
                    return label
            except FieldDoesNotExist:
                # If it is not a field, we try to find a property with that
                # name
                if field_name in dir(self.model) \
                        and isinstance(getattr(self.model,
                                               field_name), property) \
                        and field_name in self.field_labels:
                    return self.field_labels[field_name]
        return None

    def export_csv(self, request, filter_list=None, *args, **kwargs):

        now = datetime.datetime.now()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}_{}.csv' \
            .format(self.csv_filename,
                    now.strftime('%Y%m%d'))

        response.write(u'\ufeff'.encode('utf-8'))
        writer = csv.writer(response,
                            dialect='excel',
                            delimiter=str(';'),
                            quotechar=str('"'))

        # If no field was selected, we export all of them
        if filter_list is None or len(filter_list) == 0:
            filter_list = self.available_fields

        final_fields = []
        header_row = []

        for field in filter_list:
            if field in self.__csv_fields:
                header_row.append(self.__csv_fields[field])
                final_fields.append(field)

        writer.writerow(header_row)

        for elem in self.object_list:
            results = []
            for field in final_fields:
                value = getattr(elem, field)
                value = str(value).strip() if value else ''
                results.append(value)
            writer.writerow(results)

        return response

    def get_context_data(self, **kwargs):
        context = super(ExportAsCSVMixin, self).get_context_data(**kwargs)
        context['export_csv_fields'] = self.__csv_fields
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('export', '') == 'csv':
            if 'o' in request.GET:
                request.GET = request.GET.copy()
                del request.GET['o']
            filter_list = request.GET.getlist('csv_fields[]', None)
            filterset_class = self.get_filterset_class()
            self.filterset = self.get_filterset(filterset_class)
            self.object_list = self.filterset.qs

            return self.export_csv(request, filter_list, *args, **kwargs)

        return super(ExportAsCSVMixin, self).get(request, *args, **kwargs)
