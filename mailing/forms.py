from django import forms

from mailing.models import Schedule, User


class ScheduleForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        label='Choice users',
        queryset=User.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Schedule
        exclude = ['created_at', 'modified_date', 'is_active', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'users':
                field.widget.attrs['class'] = 'form-control'
