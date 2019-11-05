"""medpolls URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import polls.views.parameters
import polls.views.patients
import polls.views.polls
import polls.views.rules

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', polls.views.parameters.index, name='parameter_index'),
    path('parameters/<int:pk>/details', polls.views.parameters.details, name='parameter_details'),
    path('parameters/create', polls.views.parameters.create, name='parameter_create'),
    path('parameters/<int:pk>/edit', polls.views.parameters.edit, name='parameter_edit'),
    path('parameters/<int:pk>/delete', polls.views.parameters.delete, name='parameter_delete'),

    path('patients', polls.views.patients.index, name='patient_index'),
    path('patients/<int:pk>/details', polls.views.patients.details, name='patient_details'),
    path('patients/create', polls.views.patients.create, name='patient_create'),
    path('patients/<int:pk>/edit', polls.views.patients.edit, name='patient_edit'),
    path('patients/<int:pk>/delete', polls.views.patients.delete, name='patient_delete'),

    path('polls', polls.views.polls.index, name='poll_index'),
    path('polls/<int:pk>/details', polls.views.polls.details, name='poll_details'),
    path('polls/create', polls.views.polls.create, name='poll_create'),
    path('polls/<int:pk>/edit', polls.views.polls.edit, name='poll_edit'),
    path('polls/<int:pk>/delete', polls.views.polls.delete, name='poll_delete'),
    path('polls/<int:pk>/run', polls.views.polls.run, name='poll_run'),

    path('rules', polls.views.rules.index, name='rule_index'),
    path('rules/<int:pk>/details', polls.views.rules.details, name='rule_details'),
    path('rules/create', polls.views.rules.create, name='rule_create'),
    path('rules/<int:pk>/edit', polls.views.rules.edit, name='rule_edit'),
    path('rules/<int:pk>/delete', polls.views.rules.delete, name='rule_delete'),

]
