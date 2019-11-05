import json

from django.template.defaultfilters import register
from django.db import models
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone

from plotly.offline import plot
import plotly.graph_objs as go

from django.utils.html import mark_safe

@register.simple_tag
def check_rule(rule, patient):
    return rule.check_patient(patient)

@register.simple_tag
def parameter_plot(parameter, patient):
    return mark_safe(parameter.get_patient_plot(patient))

class Rule(models.Model):
    name = models.CharField(max_length=30, verbose_name="Имя правила")
    params = models.TextField()

    def __str__(self):
        return self.name

    def check_patient(self, patient):
        rule = json.loads(self.params)

        or_alert = False
        for or_rule in rule:
            and_rule = True

            for and_rule in or_rule:
                parameter_id = and_rule['parameter_id']
                sign = and_rule['sign']
                criteria = and_rule['criteria']
                check_value = and_rule['value']
                n = int(and_rule['n'])

                hit = False
                parameter = get_object_or_404(Parameter, pk=parameter_id)
                measurements = patient.measurement_set.filter(parameter=parameter).all()[::-1][:n]
                values = map(lambda x:x.value, measurements)
                if criteria in ['all', 'any']:
                    for value in values:
                        if criteria == 'all':
                            if sign == '=':
                                if value != check_value:
                                    hit = False
                                    break
                            if sign == '!=':
                                if value == check_value:
                                    hit = False
                                    break
                            if parameter.type == 'int':
                                if sign == '<':
                                    if int(value) >= check_value:
                                        hit = False
                                        break
                                if sign == '>':
                                    if int(value) <= check_value:
                                        hit = False
                                        break
                        elif criteria == 'any':
                            if sign == '=':
                                if value == check_value:
                                    hit = True
                                    break
                            if sign == '!=':
                                if value != check_value:
                                    hit = True
                                    break
                            if parameter.type == 'int':
                                if sign == '<':
                                    if int(value) < check_value:
                                        hit = True
                                        break
                                if sign == '>':
                                    if int(value) > check_value:
                                        hit = True
                                        break
                elif criteria in ['min', 'max', 'mean']:
                    if criteria == 'min':
                        value = min(values)
                    elif criteria == 'max':
                        value = max(values)
                    elif criteria == 'mean':
                        value = sum(values) / len(values)

                    if sign == '=':
                        if value == check_value:
                            hit = True
                    if sign == '!=':
                        if value != check_value:
                            hit = True
                    if parameter.type == 'int':
                        if sign == '<':
                            if int(value) < check_value:
                                hit = True
                        if sign == '>':
                            if int(value) > check_value:
                                hit = True

                if hit == False:
                    and_rule = False
                    break

            if and_rule:
                or_alert = True
                break

        if or_alert:
            return True
        else:
            return False


class Parameter(models.Model):
    name = models.CharField(max_length=30, verbose_name="Имя параметра")
    type = models.CharField(max_length=30, default='int',
                            choices=[('int', 'Целое число'), ('float', 'Десятичное число'), ('string', 'Строка'),
                                     ('text', 'Строка')],
                            verbose_name="Тип параметра")
    interface = models.CharField(max_length=30, default='field', choices=[('field', 'Текстовое поле')],
                                 verbose_name="Поле в опроснике")
    params = models.TextField(null=True, verbose_name="Конфигураци поля опросника")

    def __str__(self):
        return self.name

    def get_patient_plot(self, patient):
        measurements = patient.measurement_set.filter(parameter=self).all()
        time = list(map(lambda x:x.datetime, measurements))
        values = list(map(lambda x: int(x.value), measurements))

        fig = go.Figure(data=go.Scatter(x=time, y=values))
        return plot(fig, output_type='div', include_plotlyjs=False)

class Poll(models.Model):
    name = models.CharField(max_length=30, verbose_name="Имя опросника")
    parameters = models.ManyToManyField(Parameter, verbose_name="Параметры")
    days = models.TextField(verbose_name="Расписание")

    def __str__(self):
        return self.name


class Patient(models.Model):
    contract_id = models.IntegerField()
    name = models.CharField(max_length=255, verbose_name="ФИО", null=True)
    rules = models.ManyToManyField(Rule, verbose_name="Правила")
    polls = models.ManyToManyField(Poll, verbose_name="Опросники")

    def __str__(self):
        return self.name


class Measurement(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=30)
    datetime = models.DateTimeField(default=timezone.now)
