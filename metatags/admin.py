from django.contrib import admin
from .models import PageMeta
# Register your models here.


@admin.register(PageMeta)
class PageMetaAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'description']
    search_fields = ['slug', 'title']
