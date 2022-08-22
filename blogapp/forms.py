from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from blogapp.models import UserProfile,Blogs,Comments
from datetime import date



class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=[
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2"
        ]


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)



class UserProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        exclude=("user","following")
        widget={"date_of_birth":forms.DateInput(attrs={"class":"form-control","type":date}),

        }


class PasswordRestForm(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput)
    new_password=forms.CharField(widget=forms.PasswordInput)




class BlogForm(ModelForm):         #postform
    class Meta:
        model=Blogs
        fields=[          # i dont need a title for blog
            "description",
            "image"
        ]
        widgets={
                 "description":forms.Textarea(attrs={"class":"form-control","placeholder":"Write something... "}),
                 "image":forms.FileInput(attrs={"class":"form-control"})

        }

class ProfilePicUpdateForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=[
            "profile_pic"
        ]


class CommentsForm(ModelForm):
    class Meta:
        model=Comments
        fields=[
            "comment"
        ]