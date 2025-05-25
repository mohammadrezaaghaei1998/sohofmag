from django.contrib import admin
from .models import (AboutUsVideo,HomePageVideo,AboutUsImageTitle, AboutUsImages, AboutUsMainTitle, AboutUsFounder, AboutUsOurVision,
    AboutUsQualityObjectives, AboutUsKeyStrategies, AboutUsOurPolicy, AboutUsOurPolicyBox,
    AboutUsOurPolicyItems, TabSection, TabItem, HistoryItem, OurTeam, Partner
)

# Register your models here.


admin.site.register(AboutUsVideo)
admin.site.register(HomePageVideo)




admin.site.register(AboutUsImageTitle)
admin.site.register(AboutUsImages)
admin.site.register(AboutUsMainTitle)
admin.site.register(AboutUsFounder)
admin.site.register(AboutUsOurVision)
admin.site.register(AboutUsQualityObjectives)
admin.site.register(AboutUsKeyStrategies)
admin.site.register(AboutUsOurPolicy)
admin.site.register(AboutUsOurPolicyBox)
admin.site.register(AboutUsOurPolicyItems)
admin.site.register(TabSection)
admin.site.register(TabItem)
admin.site.register(HistoryItem)
admin.site.register(OurTeam)
admin.site.register(Partner)
