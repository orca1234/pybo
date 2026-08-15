from django import forms

from pybo.models import Question, Answer, Comment


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content', 'category']
        labels = {
            'subject': '제목',
            'content': '내용',
            'category': '카테고리',
        }
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': '예: Python, Django, 기타',
            }),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }