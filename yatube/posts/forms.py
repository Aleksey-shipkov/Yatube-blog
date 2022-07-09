from django import forms


from posts.models import Post, Comment
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('group', 'text', 'image')

    def clean_subject(self):
        text = self.cleaned_data['text']
        if text == '':
            raise ValidationError('А кто заполнять будет?!')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
