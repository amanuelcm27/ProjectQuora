from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from tinymce.widgets import TinyMCE


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'date_joined']
        input_formats = {
            'grad_year': ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y', '%b %d, %Y'],
            'start_year': ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y', '%b %d, %Y'],
            'end_year': ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y', '%b %d, %Y'],
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""
        self.fields['grad_year'].widget.attrs.update({'placeholder': 'YYYY-MM-DD'})
        self.fields['start_year'].widget.attrs.update({'placeholder': 'YYYY-MM-DD'})
        self.fields['end_year'].widget.attrs.update({'placeholder': 'YYYY-MM-DD'})
        self.fields["degree_type"].widget.attrs.update({"placeholder":"bachelors, masters, Phd etc ..."})


class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', "username", 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"  # Add a CSS class to each field if needed
            field.help_text = ""  # Remove the help text for each field


class QuestionForm(ModelForm):
    to = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # You can filter this queryset as needed
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Question
        fields = ["content", "topic"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"  # Add a CSS class to each field if needed
            field.help_text = ""  # Remove the help text for each field

    def save(self, commit=True):
        question = super().save(commit=False)
        question.creator = self.user  # we have set the 'user' attribute on the form in the view
        if commit:
            question.save()

        # Process selected users and link them to the question
        selected_users = self.cleaned_data['to']
        question.to.set(selected_users)

        return question


class EditQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"  # Add a CSS class to each field if needed
            field.help_text = ""  # Remove the help text for each field


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
    content = forms.CharField(widget=TinyMCE(attrs={'col': 200, "row": 100, "placeholder":"Write your answer " }))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ['name','description']
