from django.contrib import admin
from .models import (CarouselSlide,WhatWeDoCard, WhatWeDoSection,CategoryHighlightSection, 
CategoryHighlightBox,CatalogueHighlightSection,FifthSection,SixthSection,SeventhSection,EighthSection)
# Register your models here.




@admin.register(CarouselSlide)
class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'show_video_button')
    fields = ('title', 'subtitle', 'background_image', 'show_video_button', 'video', 'order')  




admin.site.register(WhatWeDoCard)
admin.site.register(WhatWeDoSection)

admin.site.register(CategoryHighlightSection)
admin.site.register(CategoryHighlightBox)

admin.site.register(CatalogueHighlightSection)

admin.site.register(FifthSection)

admin.site.register(SixthSection)

admin.site.register(SeventhSection)

admin.site.register(EighthSection)