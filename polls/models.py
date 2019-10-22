from django.db import models
from datetime import datetime

from django.utils import timezone


class Patient(models.Model):
    contract_id = models.IntegerField()
    name = models.CharField(max_length=255, verbose_name="ФИО", null=True)

    def __str__(self):
        return self.name


class Parameter(models.Model):
    name = models.CharField(max_length=30, verbose_name="Имя параметра")
    type = models.CharField(max_length=30, default='int', choices=[('int', 'Целое число'), ('float', 'Десятичное число'), ('string', 'Строка'), ('text', 'Строка')],
                            verbose_name="Тип параметра")
    interface = models.CharField(max_length=30, default='field', choices=[('field', 'Текстовое поле')],
                                 verbose_name="Поле в опроснике")
    params = models.TextField(null=True, verbose_name="Конфигураци поля опросника")

    def __str__(self):
        return self.name


class Measurement(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=30)
    datetime = models.DateTimeField(default=timezone.now)


class Poll(models.Model):
    name = models.CharField(max_length=30, verbose_name="Имя опросника")
    patients = models.ManyToManyField(Patient, verbose_name="Пациенты")
    parameters = models.ManyToManyField(Parameter, verbose_name="Параметры")
    days = models.TextField(verbose_name="Расписание")


class Rule(models.Model):
    patients = models.ManyToManyField(Patient, verbose_name="Пациенты")
    params = models.TextField()
