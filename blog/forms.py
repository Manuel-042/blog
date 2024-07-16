from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from account.models import CustomUser, Blog, Comment
from django import forms
from django.forms.widgets import TextInput, PasswordInput
from django_quill.forms import QuillFormField
from cloudinary.forms import CloudinaryFileField

class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        
#Login a user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput()) 
    password = forms.CharField(widget=PasswordInput())
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    
#Password change
class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=PasswordInput())
    new_password1 = forms.CharField(widget=PasswordInput())
    new_password2 = forms.CharField(widget=PasswordInput())
    
class BlogCreateForm(forms.ModelForm):
    # blogpost = QuillFormField()
    image = CloudinaryFileField()
    
    class Meta:
        model = Blog
        fields = ['image', 'title', 'description', 'blogpost', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Article Title...'}),
            'description': forms.TextInput(attrs={'placeholder': 'Article Description...'}),
            'category': forms.Select(attrs={'class': "form-select w-25 d-inline-block fw-bold"})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].options={
            'tags': 'new_image',
            'format': 'png'
        }

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model: Comment
        fields = ['comment']