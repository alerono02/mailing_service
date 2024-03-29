from django import forms

from mailing.models import Schedule, Client


class ScheduleForm(forms.ModelForm):
    # users = forms.ModelMultipleChoiceField(
    #     label='Choice users',
    #     queryset=Client.objects.filter(is_active=True),
    #     widget=forms.CheckboxSelectMultiple
    # )

    class Meta:
        model = Schedule
        exclude = ['created_at', 'modified_date', 'is_active', 'status', 'owner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'clients':
                field.widget.attrs['class'] = 'form-control'
