from django import forms

from newsapp.comments.models import Comment


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.user = self.request.user
        if commit:
            comment.save()
            return comment

    class Meta:
        model = Comment
        fields = ['comment_body']
