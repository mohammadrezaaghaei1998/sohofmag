from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import SellerProfile, Certification, Video,ProductImage, Product, Category, SubCategory ,CataloguePdf, CataloguePagePdf,CatalogueComment
from .utils import convert_pdf_to_images

# class SellerProfileAdmin(admin.ModelAdmin):
#     list_display = ['company_name', 'is_in_catalogue']
#     list_filter = ['is_in_catalogue']
#     search_fields = [' company_name', 'company_location']

#     def activate_in_catalogue(self, request, queryset):
#         queryset.update(is_in_catalogue=True)
#     activate_in_catalogue.short_description = "Activate selected companies in the catalogue"
    
#     def deactivate_from_catalogue(self, request, queryset):
#         queryset.update(is_in_catalogue=False)
#     deactivate_from_catalogue.short_description = "Deactivate selected companies from the catalogue"
    
#     actions = [activate_in_catalogue, deactivate_from_catalogue]



# class CatalogueAdmin(admin.ModelAdmin):
#     list_display = ['SellerProfile', 'added_on']
#     search_fields = ['company__name']

# admin.site.register(Catalogue, CatalogueAdmin)



admin.site.register(SellerProfile) 
# admin.site.register(SellerProfile,SellerProfileAdmin) 
admin.site.register(Certification)





class CataloguePageAdmin(admin.ModelAdmin):
    list_display = ('page_number', 'page_image')
    filter_horizontal = ('sellers',)

# admin.site.register(Catalogue)
# admin.site.register(CataloguePage, CataloguePageAdmin)


admin.site.register(Video)
# admin.site.register(ProductImage)
admin.site.register(Product)





class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product', 'image', 'image_title'] 

    def clean_image(self):
        image = self.cleaned_data.get('image', None)
        if not image:
            return image  #
        return image

class ProductImageAdmin(admin.ModelAdmin):
    form = ProductImageForm
    list_display = ('get_image', 'get_company_name', 'product')

    fieldsets = (
        (None, {
            'fields': ('product', 'image', 'image_title')
        }),
    )
    list_filter = ('product',)

    def get_image(self, obj):
        if obj.image:
            return format_html('<a href="{}" target="_blank"><img src="{}" style="width: 50px; height: auto;" /></a>', obj.image.url, obj.image.url)
        return "No Image"
    get_image.short_description = 'Image'
    
    def get_company_name(self, obj):
        return obj.product.SellerProfile.company_name if obj.product and obj.product.SellerProfile else 'No Company'
    get_company_name.short_description = 'Seller Company Name'

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['image']:
            obj.image = form.cleaned_data['image']  
        obj.save()

admin.site.register(ProductImage, ProductImageAdmin)




class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon') 
    search_fields = ('name', 'category__name', 'icon')  
    list_filter = ('category',) 
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'icon')
        }),
    )

admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category)










@admin.register(CataloguePdf)
class CataloguePdfAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')  

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change: 
            print(f"Converting PDF to images for catalogue {obj.title}")
            convert_pdf_to_images(obj)



admin.site.register(CataloguePagePdf)

admin.site.register(CatalogueComment)

