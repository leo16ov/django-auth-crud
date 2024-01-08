from django.forms import ModelForm
from .models import Task

class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'important']
    
