from django import forms
from django.forms import ModelForm
import models

class TaskForm(forms.Form):
    
    task_choices = models.TaskCenter._meta.get_field('task_type').choices
    
    name = forms.CharField(label='task name', max_length=100)
    description = forms.CharField()
    task_type = forms.ChoiceField(choices= task_choices,required=True)
    hosts = forms.SelectMultiple()
    groups = forms.SelectMultiple()
    content = forms.Textarea()
    kick_off_at = forms.DateTimeField()
    
class TaskCenterForm(ModelForm):
    class Meta:
        model = models.TaskCenter
        fields = ['name', 'description', 'task_type','hosts','groups','content',
                  'kick_off_at']

    def __init__(self, *args, **kwargs):
        super(TaskCenterForm, self).__init__(*args, **kwargs)
        self.fields['hosts'].widget.attrs.update({'class' : 'form-control'})
        self.fields['groups'].widget.attrs.update({'class' : 'form-control'})
        self.fields['task_type'].widget.attrs.update({'class' : 'form-control'})
        self.fields['description'].widget.attrs.update({'class' : 'form-control','placeholder':'task description','rows':3})
        self.fields['name'].widget.attrs.update({'class' : 'form-control','placeholder':'task name'})
        self.fields['content'].widget.attrs.update({'class' : 'form-control','placeholder':'task name','rows':3})
        
