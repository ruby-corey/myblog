from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author','email','body']
        widgets = {
            'author':forms.TextInput(attrs={'class':'form-control','placeholder':'请输入你的名称'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'请输入邮箱(不会公开)','required': False}),
            'body':forms.Textarea(attrs={'class':'form-control','rows':4,'placeholder':'请输入评论内容'}),
        }
        labels = {
            'author':'昵称',
            'email':'邮箱',
            'body':'评论内容',
        }