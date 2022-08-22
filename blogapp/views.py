from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from blogapp.forms import UserRegistrationForm,LoginForm,UserProfileForm,PasswordRestForm,BlogForm,ProfilePicUpdateForm,CommentsForm
from django.views.generic import View,CreateView,FormView,TemplateView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from blogapp.models import UserProfile,Blogs,Comments
from django.contrib import messages
from django.utils.decorators import method_decorator




# Create your views here.


#decoretor for authenticate

def signin_requied(fn):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"you must login")
            return redirect("signin")
    return wrapper


class SignUpView(CreateView):
    form_class=UserRegistrationForm
    template_name="registration.html"
    model=User
    success_url= reverse_lazy('signin')


class LoginView(FormView):
    model=User
    template_name="login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                print("success")
                login(request,user)
                return redirect("home")
            else:
                return render(request,self.template_name,{"form":form})

@method_decorator(signin_requied,name="dispatch")
class IndexView(CreateView):
    model = Blogs
    form_class = BlogForm
    template_name = "home.html"
    success_url = reverse_lazy("home")
    def form_valid(self, form):
        form.instance.author=self.request.user
        self.object=form.save()
        messages.success(self.request,"post has been saved")
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        blogs=Blogs.objects.all().order_by("-posted_date")
        context["blogs"]=blogs
        comment_form=CommentsForm()                #instance created
        context["comment_form"]=comment_form
        return context

@method_decorator(signin_requied,name="dispatch")
class CreateUserProfileView(CreateView):
    model=UserProfile
    template_name = "addprofile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"profile created successfully")
        self.object=form.save()
        return super().form_valid(form)

@method_decorator(signin_requied,name="dispatch")
class ViewMyprofileView(TemplateView):
    template_name = "view-profile.html"

@method_decorator(signin_requied,name="dispatch")
class PasswordResetView(FormView):
    template_name = "password-reset.html"
    form_class = PasswordRestForm

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            oldpassword=form.cleaned_data.get("old_password")
            password1=form.cleaned_data.get("confirm_password")
            user=authenticate(request,username=request.user.username,password=oldpassword)
            if user:
                user.set_password(password1)
                user.save()
                messages.success(request,"password changed")
                return redirect("signin")
            else:
                messages.error(request,"invalid input")
                return render(request,self.template_name,{"form":form})

@method_decorator(signin_requied,name="dispatch")
class ProfileUpdateView(UpdateView):
    model=UserProfile
    form_class=UserProfileForm
    template_name = "profileupdate.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        messages.success(self.request,"profile updated successfully")
        self.object=form.save()
        return super().form_valid(form)

@method_decorator(signin_requied,name="dispatch")
class ProfilepicChangeView(UpdateView):
    model = UserProfile
    form_class = ProfilePicUpdateForm
    template_name = "profilepic-update.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        messages.success(self.request,"Profile picture changed successfully")
        self.object=form.save()
        return super().form_valid(form)

@signin_requied
def add_comment(request,*args,**kwargs):
    if request.method=="POST":
        blog_id=kwargs.get("post_id")
        blog=Blogs.objects.get(id=blog_id)
        user=request.user
        comment=request.POST.get("comment")
        Comments.objects.create(blog=blog,comment=comment,user=user)          #orm query
        messages.success(request,"comment posted")
        return redirect("home")

@signin_requied
def add_like(request,*args,**kwargs):
    blog_id=kwargs.get("post_id")
    blog=Blogs.objects.get(id=blog_id)
    blog. liked_by.add(request.user)
    blog.save()
    return redirect("home")

@signin_requied
def sign_out(request,*args,**kwargs):
    logout(request)
    return redirect("signin")


def follow_friend(request,*args,**kwargs):
    friend_id=kwargs.get("user_id")
    friend_profile=User.objects.get(id=friend_id)
    request.user.users.following.add(friend_profile)
    friend_profile.save()
    return redirect("home")



# def remove_post(request,*args,**kwargs):
#     img=kwargs.get("image")
#     bimage=Blogs.objects.get("image")
#     bimage.delete()
#     messages.success(request, "post deleted successfully")
#     return redirect("home")
#
#









