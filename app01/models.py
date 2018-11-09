from django.db import models


# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    pub_date = models.DateField()
    publish = models.ForeignKey(to='Publish', on_delete=models.CASCADE)
    authors = models.ManyToManyField(to='Author')


class Publish(models.Model):
    name = models.CharField(max_length=32)
    emaill = models.CharField(max_length=32, null=True, default='Unknown')
    addr = models.CharField(max_length=32, null=True, default='Unknown')


class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField(null=True)
    ad = models.OneToOneField(to='AuthorDetail', on_delete=models.CASCADE)


class AuthorDetail(models.Model):
    profession = models.CharField(max_length=32, null=True, default='novelist')
    hobby = models.CharField(max_length=32, null=True, default='Unknown')
    tel = models.IntegerField(null=True)


class Emp(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    dep = models.CharField(max_length=32)
    province = models.CharField(max_length=32)


class User(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
