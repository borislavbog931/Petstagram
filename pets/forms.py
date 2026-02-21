from django import forms

from pets.models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'date_of_birth', 'personal_photo']

        labels = {
            'name': '',
            'date_of_birth': '',
            'personal_photo': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Pet name'}),
            'date_of_birth': forms.DateInput(attrs={'placeholder': 'Date of Birth'}),
            'personal_photo': forms.URLInput(attrs={'placeholder': 'Personal Photo'}),
        }

class PetDeleteForm(PetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
            field.widget.attrs['readonly'] = True
