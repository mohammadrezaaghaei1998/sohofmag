from django.db import models

# Create your models here.



class CarouselSlide(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField(blank=True, null=True)
    background_image = models.ImageField(upload_to='carousel/')
    show_video_button = models.BooleanField(default=False)
    video = models.FileField(upload_to='carousel/videos/', blank=True, null=True) 
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title




class WhatWeDoSection(models.Model):
    heading = models.CharField(max_length=255, default="What we do?")
    paragraph = models.TextField()

    def __str__(self):
        return self.heading




class WhatWeDoCard(models.Model):
    icon_class = models.CharField(max_length=100) 
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title





class CategoryHighlightSection(models.Model):
    heading = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.heading

class CategoryHighlightBox(models.Model):
    section = models.ForeignKey(CategoryHighlightSection, on_delete=models.CASCADE, related_name='boxes')
    number = models.CharField(max_length=50)  
    label = models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.number} {self.label}"





class CatalogueHighlightSection(models.Model):
    heading = models.CharField(max_length=255)
    description = models.TextField()
    first_image = models.ImageField(upload_to='catalogue_highlight/')
    second_image = models.ImageField(upload_to='catalogue_highlight/')
    

    def __str__(self):
        return self.heading





class FifthSection(models.Model):
    headtitle = models.CharField(max_length=255)

    title_left = models.CharField(max_length=255)
    subtitle_left = models.CharField(max_length=255, blank=True)
    description_left = models.TextField()
    icon_left = models.ImageField(upload_to='catalogue_icons/')

    title_right = models.CharField(max_length=255)
    subtitle_right = models.CharField(max_length=255, blank=True)
    description_right = models.TextField()
    icon_right = models.ImageField(upload_to='catalogue_icons/')

    def __str__(self):
        return "Catalogue Highlight Section"









class SixthSection(models.Model):
    main_title = models.CharField(max_length=255)

    title1 = models.CharField(max_length=255)
    description1 = models.TextField()
    image1 = models.ImageField(upload_to='sixth_section/')  

    title2 = models.CharField(max_length=255)
    description2 = models.TextField()
    image2 = models.ImageField(upload_to='sixth_section/')  

    title3 = models.CharField(max_length=255)
    description3 = models.TextField()
    image3 = models.ImageField(upload_to='sixth_section/')  

    title4 = models.CharField(max_length=255)
    description4 = models.TextField()
    image4 = models.ImageField(upload_to='sixth_section/') 

    title5 = models.CharField(max_length=255)
    description5 = models.TextField()
    image5 = models.ImageField(upload_to='sixth_section/')  

    def __str__(self):
        return f"Sixth Section: {self.main_title}"




class SeventhSection(models.Model):
    background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    heading = models.CharField(max_length=255)
    subheading = models.CharField(max_length=255)
    button_text = models.CharField(max_length=100)
    button_link = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.heading
    


class EighthSection(models.Model):
    heading = models.CharField(max_length=255)
    subheading = models.TextField()

    left_title = models.CharField(max_length=100)
    left_content = models.TextField()
    left_image = models.ImageField(upload_to='eighthsection/left/', blank=True, null=True)

    right_first_title = models.CharField(max_length=100)
    right_first_content = models.TextField()
    right_first_image = models.ImageField(upload_to='eighthsection/right_first/', blank=True, null=True)

    right_second_title = models.CharField(max_length=100)
    right_second_content = models.TextField()
    right_second_image = models.ImageField(upload_to='eighthsection/right_second/', blank=True, null=True)

    def __str__(self):
        return self.heading
