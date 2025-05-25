from django.db import models

# Create your models here.




class PageMeta(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)

    robots = models.CharField(max_length=100, blank=True, null=True)
    
   
    og_title = models.CharField(max_length=255, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    og_image = models.ImageField(upload_to='meta/Open Graph/', blank=True, null=True)
    og_url = models.URLField(blank=True, null=True)

   
    twitter_title = models.CharField(max_length=255, blank=True, null=True)
    twitter_description = models.TextField(blank=True, null=True)
    twitter_image = models.ImageField(upload_to='meta/twitter/', blank=True, null=True)
    twitter_card = models.CharField(max_length=50, blank=True, null=True, default="summary_large_image")
    twitter_site = models.CharField(max_length=255, blank=True, null=True) 

    canonical_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.slug
