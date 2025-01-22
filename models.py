from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


# Create your models here.
class signup(models.Model):
    name=models.CharField(max_length=50)
    username=models.CharField(max_length=200)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=200)
    confirm_password=models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
    
class signin(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    confirm_password=models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.username
    

class Sports(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
    
class Post(models.Model):
    TYPES=(
        ("1","SUMMER SPORTS"),
        ("2","WINTER SPORTS")
    )
    SECTION=(
        ("main",",main"),
        ("Popular","Popular"),
        ("Recent","Recent"),
        ("Trending","Trending"),
        ("Latest Post","Latest Post")

    )

    title=models.CharField(max_length=100)
    desc=RichTextField()
    image=models.ImageField(upload_to="image")
    sports=models.ForeignKey(Sports, verbose_name=("Type of sporst"), on_delete=models.CASCADE)
    slug=models.SlugField(max_length=200,null=True,blank=True,unique=True)
    date=models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    section=models.CharField(choices=SECTION,max_length=200)
    main_post=models.BooleanField(default=False)
    type=models.CharField(choices=TYPES,max_length=200,default="SUMMER")
  
    def __str__(self) -> str:
        return self.title
    
def create_slug(instance,new_slug=None):
    slug=slugify(instance.title)
    if new_slug is not None:
        slug=new_slug
    qs=Post.objects.filter(slug=slug).order_by('-id')
    exits=qs.exists()

    if exits:
        new_slug="%s-%s" %(slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug

def pre_save_post_reciver(sender,instance,*args, **kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)
    pre_save.connect(pre_save_post_reciver,Post)


class Comment(models.Model):
    name=models.CharField(max_length=50)
    comment=models.TextField()
    date=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
class Contact_form(models.Model):
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    email=models.EmailField()
    phone=PhoneNumberField()
    message=models.TextField(default=None)

    def __str__(self) -> str:
        return self.fname
    


class Events(models.Model):
    event = models.TextField(max_length=500 , blank=True, null=True)
    url = models.URLField(max_length=1000,blank=True, null=True)
    poster = models.ImageField(upload_to='images/', blank=True, null=True)
    description = models.TextField(max_length=5000, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.event}"
    
class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    description = models.TextField(max_length=5000)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    views =  models.IntegerField( default=0)
    likes =  models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.description}"



    

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(default="Sujan",max_length=200,null=True)
    title=models.CharField(default="this is default",max_length=200)
    desc=models.CharField(default="hello k xa",max_length=200,null=True)
    image=models.ImageField(upload_to='images',default='images/logo.png')
   

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"
    







