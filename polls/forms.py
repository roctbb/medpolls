from django.forms import ModelForm, Form
from django import forms
from django.shortcuts import get_object_or_404

from polls.models import *


class ParameterForm(ModelForm):
    class Meta:
        model = Parameter
        fields = ['name', 'type', 'interface']


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'


class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = '__all__'


class PollRunForm(ModelForm):
    class Meta:
        model = Poll
        fields = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parameters = self.instance.parameters.all()
        for parameter in parameters:
            field_name = 'parameter_%s' % (parameter.id,)
            if parameter.interface == 'field':
                if parameter.type == 'int':
                    self.fields[field_name] = forms.IntegerField(label=parameter.name)
                if parameter.type == 'float':
                    self.fields[field_name] = forms.FloatField()
                if parameter.type == 'string':
                    self.fields[field_name] = forms.CharField()
                if parameter.type == 'text':
                    self.fields[field_name] = forms.Textarea()
            try:
                self.initial[field_name] = args[0][field_name]
            except:
                self.initial[field_name] = ""

        patients = list(Patient.objects.all())
        choices = list(map(lambda x: (x.id, x.name), patients))
        self.fields['patient_id'] = forms.ChoiceField(choices=choices, label="Пациент")

    def save(self, commit=True):
        parameters = self.instance.parameters.all()
        patient = get_object_or_404(Patient, pk=self.cleaned_data['patient_id'])
        for parameter in parameters:
            field_name = 'parameter_%s' % (parameter.id,)
            measurement = Measurement()
            measurement.patient = patient
            measurement.value = str(self.cleaned_data[field_name])
            measurement.parameter = parameter
            measurement.save()

