from django.db import models

# Create your models here.

class Actor(models.Model):
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.name} {self.last_name}'

class Country(models.Model):
    name = models.CharField(max_length=20)
    iso_code = models.CharField(max_length=3)

    def __str__(self):
        return f'{self.name}'

class Movie(models.Model):
    title = models.CharField(max_length=50)
    genre = models.CharField(max_length=20)
    year = models.PositiveSmallIntegerField()
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, null=True, blank=True, related_name='movies')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, related_name='movies')

class Oscar(models.Model):
    category = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, null=True, blank=True, related_name='oscars')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, related_name='oscars')

