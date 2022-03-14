from django.forms import ModelForm

from saberworks.models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['project', 'title', 'text', 'image', 'user']

class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image']

class PostSetImageForm(ModelForm):
    class Meta:
        model = Post
        fields = ['image']
