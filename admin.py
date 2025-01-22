from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['id','title','image','sports','slug','date','section','main_post']
    list_editable=['section','main_post']
    search_fields=['title','section']
@admin.register(signup)
class signupAdmin(admin.ModelAdmin):
    list_display=['id','name','username','email','password','confirm_password']
@admin.register(signin)
class signinAdmin(admin.ModelAdmin):
    list_display=['id','username','password','confirm_password']

admin.site.register(Sports)
admin.site.register(Comment)

@admin.register(Contact_form)
class contactAdmin(admin.ModelAdmin):
    list_display=['id','fname','lname','email','phone',"message"]

admin.site.register(Profile)
admin.site.register(Events)
admin.site.register(Video)
