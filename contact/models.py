from django.db import models

# Create your models here.




class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"




class ContactUsHeader(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()

    def __str__(self):
        return self.title
    

class ContactInfo(models.Model):
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=500)

    def __str__(self):
        return f"Contact Info {self.id}"
    

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()

    def __str__(self):
        return self.question
    

class Map(models.Model):
    iframe = models.TextField("Google Maps iframe")

    def __str__(self):
        return "Map Location"