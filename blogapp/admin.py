from django.contrib import admin


# Register your models here.
from blogapp.models import Blogs,Comments,UserProfile

admin.site.register(Blogs)
admin.site.register(Comments)
admin.site.register(UserProfile)
