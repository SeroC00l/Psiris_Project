from django import forms
from .models import Task, TodoList
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    todo_list = forms.ModelChoiceField(
        queryset=TodoList.objects.all(),
        widget=forms.HiddenInput(),
    )


    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority']
        labels = {
            'title': 'Tittle',
            'description': 'Description',
            'due_date': 'Due Date',
            'priority': 'Priority'
        }
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'datetime-local'})
        }


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority']
        labels = {
            'title': 'Tittle',
            'description': 'Description',
            'due_date': 'Due Date',
            'priority': 'Priority'
        }
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'datetime-local'})
}



class ColorField(forms.CharField):
    widget = forms.TextInput(attrs={
        'type': 'color'
    })

class TodoListForm(forms.ModelForm):
    color = ColorField()

    class Meta:
        model = TodoList
        fields = ['title', 'color']
        labels = {'title': 'Title', 'color': 'Color'}


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
