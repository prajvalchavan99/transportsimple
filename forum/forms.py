from django import forms
from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Your question title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Optional details', 'class': 'form-control', 'rows': 4}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Write your answer...', 'class': 'form-control', 'rows': 4}),
        }