from django.db import models

# Create your models here.




class AboutUsVideo(models.Model):
    about_us_video = models.FileField(upload_to='about_us_videos/', blank=True, null=True)

    def __str__(self):
        return str(self.about_us_video)  

class HomePageVideo(models.Model):
    home_page_video = models.FileField(upload_to='home_page_video/', blank=True, null=True)

    def __str__(self):
        return str(self.home_page_video)  



class AboutUsImageTitle(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title



class AboutUsImages(models.Model):
    image = models.ImageField(upload_to='section_images/')

    def __str__(self):
        return f"Image {self.id}"


class AboutUsMainTitle(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class AboutUsFounder(models.Model):
    foundedby = models.CharField(max_length=255)

    def __str__(self):
        return self.foundedby


class AboutUsOurVision(models.Model):
    our_vision = models.CharField(max_length=1000)

    def __str__(self):
        return self.our_vision


class AboutUsQualityObjectives (models.Model):
    quality_objectives = models.CharField(max_length=255)

    def __str__(self):
        return self.quality_objectives


class AboutUsKeyStrategies (models.Model):
    key_strategies = models.CharField(max_length=255)

    def __str__(self):
        return self.key_strategies



class AboutUsOurPolicy (models.Model):
    our_policy = models.CharField(max_length=1000)

    def __str__(self):
        return self.our_policy


class AboutUsOurPolicyBox (models.Model):
    our_policy_box = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.our_policy_box



class AboutUsOurPolicyItems (models.Model):
    our_policy_items = models.CharField(max_length=255)
    

    def __str__(self):
        return self.our_policy_items






class TabSection(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class TabItem(models.Model):
    section = models.ForeignKey(TabSection, on_delete=models.CASCADE, related_name='tabs')
    icon_class = models.CharField(max_length=100)
    paragraph1 = models.TextField()
    paragraph2 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.section.title} - {self.icon_class}"
    







class HistoryItem(models.Model):
    year = models.CharField(max_length=10)
    label = models.TextField()

    def __str__(self):
        return f"{self.year} - {self.label[:30]}"
    






class OurTeam(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team_images/', default='team_images/default.jpg') 
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    google_plus_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    


class Partner(models.Model):
    logo = models.ImageField(upload_to='partners_logos/')

    def __str__(self):
        return f"Partner {self.id}"