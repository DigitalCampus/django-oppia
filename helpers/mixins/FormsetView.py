from django.forms import formset_factory, ModelForm
from django.views.generic.edit import FormMixin


class FormsetView(FormMixin):
    """
    A mixin to manage a view with formsets
    """

    update_formset_after_save = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formsets = self.get_named_formsets()
        forms = {}
        for name, formset in formsets.items():
            formset_initial_func = getattr(self, 'formset_{0}_get_initial'.format(name), None)
            initial = [] if formset_initial_func is None else formset_initial_func()
            forms[name] = self.get_formset_instance(formset, initial=initial)
        context['formsets'] = forms
        return context

    def get_formset_instance(self, form_dict, initial=None, **kwargs):
        if initial:
            kwargs.update({'initial': initial})
        kwargs.update(form_dict['kwargs'])

        return formset_factory(form_dict['form'])(**kwargs)

    def get_named_formsets(self):
        return []

    # Optionally implement this method
    def post_form_valid(self, form):
        pass

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        for name, formset in named_formsets.items():
            formset_instance = self.get_formset_instance(formset, data=self.request.POST, files=self.request.FILES)
            if not formset_instance.is_valid():
                errors = formset_instance.errors
                print(errors)
                print('invalid formset!!')
                return self.form_invalid(form)

        if isinstance(form, ModelForm):
            self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_instance = self.get_formset_instance(formset, data=self.request.POST, files=self.request.FILES)
            if formset_instance.is_valid():
                formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
                if formset_save_func is not None:
                    formset_save_func(form, formset_instance)
                else:
                    formset_instance.save()

        self.post_form_valid(form)

        return super().form_valid(form)
