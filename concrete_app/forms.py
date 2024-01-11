from django import forms
from .models import Modelpredictions

class Predictionform(forms.ModelForm):
    cement = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm'}))
    blast_furnace_slag = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm'}))
    fly_ash = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm'}))
    water = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm'}))
    superplasticizer = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm'}))
    coarse_aggregate = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm'}))
    fine_aggregate = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm'}))
    age = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm'}))
    class Meta:
        model = Modelpredictions
        fields = ['cement','blast_furnace_slag','fly_ash','water','superplasticizer','coarse_aggregate','fine_aggregate','age']
        
        
class Predictionfileform(forms.Form):
    upload_file = forms.FileField()