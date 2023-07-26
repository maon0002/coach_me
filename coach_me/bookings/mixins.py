from django.apps import apps


class DisabledFormFieldsMixin:
    disabled_fields = ()

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        # fields = self.disabled_fields \
        # if self.disabled_fields != '__all__' \
        # else

        for field in self.disabled_fields:
            form.fields[field].widget.attrs['disabled'] = 'disabled'
            form.fields[field].widget.attrs['readonly'] = 'readonly'

        return form


class MyModelMixin:
    @staticmethod
    def get_distinct_choices(model_name, field_name):
        model_class = apps.get_model(model_name)
        choices = tuple(model_class.objects.values_list(field_name, field_name).distinct())
        choices_list = list(model_class.objects.values_list(field_name).distinct())
        max_len = max(len(str(value)) for value in choices_list)
        return max_len, choices
