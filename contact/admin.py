from django.contrib import admin
from .models import ContactUs,ContactUsHeader,ContactInfo,FAQ,Map

# Register your models here.



admin.site.register(ContactUs)
admin.site.register(ContactUsHeader)
admin.site.register(ContactInfo)
admin.site.register(FAQ)
admin.site.register(Map)
