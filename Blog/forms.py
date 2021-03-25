from django import forms
from Blog.models import Post, Comment

# Create your forms here.
class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')  ### This provides the fields that the form creates an opportunity for user to edit

        ### Setting up CSS widgets
        widgets = {
                'title':forms.TextInput(attrs = {'class':'textinputclass'}),
                'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')  ### This provides the fields that the form creates an opportunity for user to edit

        ### Setting up CSS widgets
        widgets = {
            'author':forms.TextInput(attrs = {'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
        }
