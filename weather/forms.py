from django import forms

from .services import get_coordinates


class TemperatureForms(forms.Form):
    email = forms.EmailField(
        max_length=255,
        label='E-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'Type your email'}),
    )
    place = forms.CharField(
        max_length=255,
        label='Local',
        widget=forms.TextInput(attrs={'placeholder': 'Type a city name'}),
    )
    max_temperature = forms.IntegerField(
        label='Max temperature',
        widget=forms.NumberInput(attrs={'placeholder': 'Type the maximum temperature'}),
    )
    interval = forms.ChoiceField(
        choices=[
            (1, '1 minutes'),
            (15, '15 minutes'),
            (30, '30 minutes'),
            (45, '45 minutes'),
            (60, '1 hour'),
        ],
        widget=forms.Select(),
    )

    def clean_place(self):
        place = self.cleaned_data['place'].strip()

        if not place:
            raise forms.ValidationError('Local é obrigatório.')

        try:
            self._coordinates = get_coordinates(place)
        except Exception as e:
            raise forms.ValidationError(f'Não foi possível encontrar o local: {e}')

        return place

    def clean_interval(self):
        interval = self.cleaned_data['interval']
        return int(interval)

    def get_coordinates(self):
        return getattr(self, '_coordinates', None)
