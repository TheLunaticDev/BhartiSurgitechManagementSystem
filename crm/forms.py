from django import forms
from dal import autocomplete
from .models import (
    State, District, Area, Doctor,
)

class AreaModelForm(forms.ModelForm):
    state = forms.ModelChoiceField(queryset=State.objects.all(), label='State')
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        widget=autocomplete.ModelSelect2(url='district-autocomplete', forward=['state']),
        label='District'
    )
    area = forms.CharField(label="Area", max_length=150)

    class Meta:
        model = Area
        fields = ['state', 'district', 'area']

    def save(self, commit=True):
        cleaned_district = self.cleaned_data['district']
        cleaned_area = self.cleaned_data['area']
        area_instance = Area(district=cleaned_district, name=cleaned_area)

        if commit:
            area_instance.save()
        
        return area_instance

    def save_m2m(self):
        pass



class DoctorInlineForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'speciality', 'designation', 'email', 'phone_number']