from django.urls import path
from . import views

urlpatterns = [
   
    # path('seller-detail/<int:seller_id>/', views.seller_detail, name='seller_detail'),
    # path('seller-detail/<slug:company_name>/', views.seller_detail, name='seller_detail'),
    path('seller-detail/<slug:company_slug>/', views.seller_detail, name='seller_detail'),

    path('seller-dashboard', views.seller_dashboard, name='seller_dashboard'),
    path('company-registeration', views.company_registeration, name='company_registeration'),
    path('company-signup', views.company_signup, name='company_signup'),
    path('company-login', views.company_login, name='company_login'),
    path('seller_change_password/', views.seller_change_password, name='seller_change_password'),
    path('restriction', views.restriction, name='restriction'),

    path('submit-business-info/', views.submit_business_info, name='submit_business_info'),
    path('manage-documents/', views.manage_documents, name='manage_documents'),
    path('manage-certifications/', views.manage_certifications, name='manage_certifications'),
    path('remove_certification/<int:cert_id>/', views.remove_certification, name='remove_certification'),


    path('add_video/', views.add_video, name='add_video'),
    path('remove_video/<int:video_id>/', views.remove_video, name='remove_video'),



    path('add-product/', views.add_product, name='add_product'),
    path('remove-product/<int:product_id>/', views.remove_product, name='remove_product'),
    path('edit-product/', views.edit_product, name='edit_product'),


    path('get_subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),



    path('subcategory/<int:subcategory_id>/<slug:subcategory_name>/', views.subcategory_products_view, name='subcategory_products'),


    path('catalogues-list/', views.catalogue_list, name='catalogue_list'),
    path('catalogues-detail/<int:pk>/', views.catalogue_detail, name='catalogue_detail'),
    path('catalogue-page/<int:pk>/', views.catalogue_page_detail, name='catalogue_page_detail'),
    path('catalogue_download/<int:catalogue_id>/', views.download_catalogue, name='catalogue_download'),
    path('catalogue_increment/<int:catalogue_id>/', views.increment_download_count, name='increment_download_count'),
    path('catalogue/<int:catalogue_id>/increase-view/', views.increase_catalogue_view, name='increase_catalogue_view'),

]


