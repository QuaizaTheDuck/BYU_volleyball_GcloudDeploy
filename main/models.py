from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    latestnews = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Zespol(models.Model):
    imienazwisko = models.CharField(max_length=50)
    pozycja = models.CharField(max_length=50)
    zdjecie = models.ImageField(upload_to='zespol/', null=True, blank=True)

    def __str__(self):
        return self.imienazwisko
    
class Mecze(models.Model):
    data = models.DateField()
    godzina = models.TimeField()
    gospodarz = models.CharField(max_length=100)
    logo_gospodarza = models.ImageField(upload_to='logos/')
    wynik = models.CharField(max_length=10, blank=True, null=True)  # Pole wyniku
    przeciwnik = models.CharField(max_length=100)
    logo_przeciwnika = models.ImageField(upload_to='logos/')

    @staticmethod
    def ostatni_mecz():
        return Mecze.objects.filter(wynik__isnull=False).order_by('-data').first()

    @staticmethod
    def najblizszy_mecz():
        return Mecze.objects.filter(data__gt=timezone.now()).order_by('data').first()

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ContactEntry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.email}"