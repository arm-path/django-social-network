from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField

from .models import Post


class PostForm(forms.ModelForm):
    content = RichTextUploadingFormField()

    class Meta:
        model = Post
        fields = ['title', 'content', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title-post'}),
            'content': CKEditorUploadingWidget()
        }
