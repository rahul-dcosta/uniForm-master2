from django.db import models
# Models are basically a blueprint for your database.


class School(models.Model): # Image school as being a table
	title = models.CharField(max_length=100) # That table only has one column which is title

class account(models.Model):
	fullname = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	schools = models.ManyToManyField(School) # ManyToMany Field is an important data type to understand.


# For foreign key, that specific data entry will be of a type of another class.
# I'll give an example.
# Image the class student. It looks as such:
# class Student:
#	name = charfield
# 	age = int field
#  	school = char field
# In this example, school could be char field but I could also create another class School. This will give my
# database a little more depth. That would be an example of foreign key.
# Now a problem arises where you want to store the subjects of a student. If this was just a regular class,
# you could just create an attribute which is a list. You can't do this with databases atleast in django.
# To do this, they created a field called many to many.
# What we'll do is create a class for subject.
# It can look like this:
# class subject:
#	title = char field
#	requiredBook = char field
# So there'll be multiple of these subject objects for all different objects.
# Now in the student object, we have a many to many field for a subject. Many to many basically means
# one student objects can be linked with many subject objects. but a subject object can also be linked with
# many student objects.
