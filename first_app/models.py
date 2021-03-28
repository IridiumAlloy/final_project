from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = ("Invalid email address!")
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters.'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must contain at least 8 characters.'
        if postData['password'] != postData['confirm_pw']:
            errors['password'] = "Password and Confirm Password do not match."
        if User.objects.filter(email = postData['email']):
            errors['email'] = 'That email is already attached to another account.'
        return errors
    def second_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = ("Invalid email address!")
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters.'
        if User.objects.filter(email = postData['email']):
            errors['email'] = 'That email is already attached to another account.'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    email = models.CharField(max_length= 100)
    password = models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class State(models.Model):
    name = models.CharField(max_length=100, unique = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Statute(models.Model):
    name = models.CharField(max_length=100)
    states = models.ForeignKey(State, related_name="statutes", on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subsection(models.Model):
    citation = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    language = models.TextField()
    statutes = models.ForeignKey(Statute, related_name="subsections", on_delete= models.CASCADE)
    state = models.CharField(max_length=100, default="Illinois")
    user_likes = models.ManyToManyField(User,related_name="liked_subsections")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
