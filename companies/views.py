from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import (SellerSignupForm, SellerLoginForm,  SellerProfileUpdateForm,SellerProfileDocumentUpdateForm,
                     CertificationForm, SellerSignupForm, VideoForm ,
                     ProductForm, ProductImageForm,CatalogueCommentForm)
from accounts.models import CustomUser
from .models import SellerProfile, Certification, SellerProfile, CataloguePdf, CataloguePagePdf, Video, Product, ProductImage,Category, SubCategory,ProfileViewLog
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import F
from socialmedia.models import SocialMediaLinks
from django.contrib.auth import logout

import os
from django.http import FileResponse, Http404 ,JsonResponse
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
from django.core.paginator import Paginator

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from pdf2image import convert_from_path
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from io import BytesIO
import os
from metatags.models import PageMeta
from django.utils.text import slugify



User = get_user_model()
# Create your views here.


def company_registeration(request):
    return render(request, 'companies/company_registeration.html')





def company_signup(request):
    meta = PageMeta.objects.filter(slug="company_signup").first()
    if request.user.is_authenticated:  
        return render(request, "companies/signup_restricted.html")  
    if request.method == "POST":
        form = SellerSignupForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():  
                    user = form.save(commit=False)  
                    user.user_type = "seller" 
                    user.save()  
                    
                    extra_fields = {field: form.cleaned_data[field] for field in form.cleaned_data if field not in ["password1", "password2", "username"]}
                    extra_fields['slug'] = slugify(extra_fields['company_name'])    
                    SellerProfile.objects.create(user=user, **extra_fields)

                messages.success(request, "Signup successful! You can now log in.")
                return redirect("index") 
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}") 

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    else:
        form = SellerSignupForm()
    
    return render(request, 'companies/company_signup.html', {"form": form,'meta': meta})



# def company_login(request):
#     meta = PageMeta.objects.filter(slug="company_login").first()
#     if request.user.is_authenticated:
#         if request.user.user_type == "seller":
#             return redirect("seller_dashboard")
#         else:
#             logout(request)

#     if request.method == "POST":
#         form = SellerLoginForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             if user.user_type == "seller":
#                 login(request, user)
#                 messages.success(request, f"Welcome back, {user.username}!")
#                 return redirect("seller_dashboard")
#             else:
#                 messages.error(request, "Invalid seller credentials.")
#         else:
#             messages.error(request, "Invalid username or password.")
#     else:
#         form = SellerLoginForm()
#     return render(request, 'companies/company_login.html', {"form": form,'meta': meta})






def company_login(request):
    meta = PageMeta.objects.filter(slug="company_login").first()
    if request.user.is_authenticated:
        if request.user.user_type == "seller":
            return redirect("seller_dashboard")
        else:
            logout(request)

    if request.method == "POST":
        form = SellerLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.user_type == "seller":
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("seller_dashboard")
            else:
                messages.error(request, "Invalid seller credentials.")
        else:
            if form.errors.get('captcha'):
                messages.error(request, "Invalid captcha. Please try again.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = SellerLoginForm()
    return render(request, 'companies/company_login.html', {"form": form, 'meta': meta})




@login_required
def seller_change_password(request):
    if request.user.user_type != 'seller':  
        return redirect('index') 

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()  
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('seller_dashboard')  
        else:
            print(form.errors)  
            messages.error(request, 'There was an error with your password change.')
    else:
        form = PasswordChangeForm(request.user) 

    return render(request, 'companies/seller_dashboard.html', {'form': form})







def submit_business_info(request):
    sellerprofile = SellerProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = SellerProfileUpdateForm(request.POST, request.FILES, instance=sellerprofile)
        if form.is_valid():
            form.save()
            messages.success(request, "Business info updated successfully.")
        else:
            messages.error(request, "There was an error updating your business info.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        return redirect('seller_dashboard')
    
    else:
        form = SellerProfileUpdateForm(instance=sellerprofile)

    return render(request, 'companies/seller_dashboard.html', {'form': form, 'sellerprofile': sellerprofile})






def manage_documents(request):
    sellerprofile = SellerProfile.objects.get(user=request.user)

    if request.method == 'POST':
        try:
            if 'remove_company_logo' in request.POST:
                sellerprofile.company_logo.delete()
                sellerprofile.save()
                messages.success(request, 'Company logo removed successfully.')
        except Exception as e:
            messages.error(request, f'Error removing company logo: {e}')

        try:
            if 'remove_company_license' in request.POST:
                sellerprofile.company_license.delete()
                sellerprofile.company_license = 'uploads/company_licenses/default_license.pdf'
                sellerprofile.save()
                messages.success(request, 'Company license removed successfully.')
        except Exception as e:
            messages.error(request, f'Error removing company license: {e}')

        try:
            if 'remove_tax_registration' in request.POST:
                sellerprofile.tax_registration.delete()
                sellerprofile.save()
                messages.success(request, 'Tax registration removed successfully.')
        except Exception as e:
            messages.error(request, f'Error removing tax registration: {e}')

        try:
            if 'remove_utility_bill' in request.POST:
                sellerprofile.utility_bill.delete()
                sellerprofile.save()
                messages.success(request, 'Utility bill removed successfully.')
        except Exception as e:
            messages.error(request, f'Error removing utility bill: {e}')

        try:
            if 'remove_bank_statement' in request.POST:
                sellerprofile.bank_statement.delete()
                sellerprofile.save()
                messages.success(request, 'Bank statement removed successfully.')
        except Exception as e:
            messages.error(request, f'Error removing bank statement: {e}')

        try:
            if 'remove_id_card' in request.POST:
                sellerprofile.id_card.delete()
                sellerprofile.save()
                messages.success(request, 'ID Card removed successfully.')
        except Exception as e:
            messages.error(request, f'Error removing ID card: {e}')

        try:
            if 'remove_passport' in request.POST:
                sellerprofile.passport.delete()
                sellerprofile.save()
                messages.success(request, 'Passport removed successfully.')
        except Exception as e:
            messages.error(request, f'Error removing passport: {e}')

        document_form = SellerProfileDocumentUpdateForm(request.POST, request.FILES, instance=sellerprofile)

        if document_form.is_valid():
            document_form.save()
            messages.success(request, 'Documents updated successfully.')
            return redirect('seller_dashboard')
        else:
            error_messages = []
            for field, errors in document_form.errors.items():
                for error in errors:
                    readable_field = field.replace('_', ' ').title()
                    error_messages.append(f"{readable_field}: {error}")
            messages.error(request, " " + " | ".join(error_messages))
            return redirect('seller_dashboard')

    else:
        document_form = SellerProfileDocumentUpdateForm(instance=sellerprofile)

    return render(request, 'companies/seller_dashboard.html', {
        'document_form': document_form,
        'sellerprofile': sellerprofile
    })








def manage_certifications(request):
    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES)
        if form.is_valid():
            sellerprofile = SellerProfile.objects.filter(user=request.user).first()
            certification = form.save(commit=False)
            certification.SellerProfile = sellerprofile
            certification.save()
            messages.success(request, "Certificate added successfully!")
            return redirect('seller_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    readable_field = field.replace('_', ' ').capitalize()
                    messages.error(request, f"{readable_field}: {error}")
                    return redirect('seller_dashboard')
    else:
        form = CertificationForm()

    return render(request, 'companies/seller_dashboard.html', {'form': form})






def remove_certification(request, cert_id):
    certification = Certification.objects.filter(id=cert_id).first()
    if certification:
        certification.delete()
        messages.success(request, "Certificate removed successfully.")
    else:
        messages.error(request, "Certificate not found.")
    
    return redirect('seller_dashboard')









# def catalogues(request):
#     socialmedia = SocialMediaLinks.objects.all()
#     sort_option = request.GET.get('sort', 'newest')  
#     if sort_option == "most_downloaded":
#         catalogues = Catalogue.objects.all().order_by('-download_count')
#     elif sort_option == "most_viewed":
#         catalogues = Catalogue.objects.all().order_by('-view_count')
#     else:  
#         catalogues = Catalogue.objects.all().order_by('-publish_date')

#     total_catalogues = catalogues.count() 
#     latest_catalogues = Catalogue.objects.all().order_by('-publish_date')[:3]

#     return render(request, 'companies/catalogues.html', {
#         'catalogues': catalogues,
#         'total_catalogues': total_catalogues,
#         'sort_option': sort_option,
#         'socialmedia' : socialmedia,
#         'latest_catalogues': latest_catalogues
#     })


# def catalogue_detail(request, catalogue_id):
#     socialmedia = SocialMediaLinks.objects.all()
#     catalogue = get_object_or_404(Catalogue, id=catalogue_id)
#     pages = catalogue.catalogue_pages.all()  
#     return render(request, 'companies/catalogue_detail.html', {'catalogue': catalogue, 'pages': pages ,  'socialmedia' : socialmedia})


# def page_detail(request, page_id):
#     socialmedia = SocialMediaLinks.objects.all()
#     page = get_object_or_404(CataloguePage, id=page_id)
#     sellers = page.sellers.all() 
#     return render(request, 'companies/page_detail.html', {'page': page, 'sellers': sellers,'socialmedia' : socialmedia})




# def download_catalogue(request, catalogue_id):
#     catalogue = get_object_or_404(Catalogue, id=catalogue_id)
    
#     Catalogue.objects.filter(id=catalogue_id).update(download_count=F('download_count') + 1)

#     pages = catalogue.catalogue_pages.all() 

#     if not pages.exists():
#         raise Http404("No pages found for this catalogue.")

#     buffer = BytesIO()
#     pdf = canvas.Canvas(buffer, pagesize=A4)

#     for page in pages:
#         if page.page_image: 
#             image_path = os.path.join(settings.MEDIA_ROOT, str(page.page_image))
            
#             if os.path.exists(image_path): 
#                 img = Image.open(image_path)
#                 img_width, img_height = img.size

#                 a4_width, a4_height = A4
#                 aspect_ratio = img_width / img_height
#                 new_width = a4_width
#                 new_height = new_width / aspect_ratio
#                 if new_height > a4_height:
#                     new_height = a4_height
#                     new_width = new_height * aspect_ratio

#                 x = (a4_width - new_width) / 2
#                 y = (a4_height - new_height) / 2

#                 pdf.drawImage(image_path, x, y, width=new_width, height=new_height)
#                 pdf.showPage()

#     pdf.save()
#     buffer.seek(0)

#     filename = f"{catalogue.creator}-catalogue.pdf"
#     return FileResponse(buffer, as_attachment=True, filename=filename)



# def increase_catalogue_view(request, catalogue_id):
#     catalogue = get_object_or_404(Catalogue, id=catalogue_id)
#     catalogue.view_count += 1
#     catalogue.save()
#     return JsonResponse({"view_count": catalogue.view_count})













# def seller_detail(request, seller_id):
#     meta = PageMeta.objects.filter(slug="seller_detail").first()
#     socialmedia = SocialMediaLinks.objects.all()
#     seller = get_object_or_404(SellerProfile, id=seller_id)
#     ProfileViewLog.objects.create(seller=seller)
#     seller.update_views()
#     if seller.profile_views > 50:
#         seller.is_verified = True
#     if seller.profile_views > 100:
#         seller.is_gold = True
#     seller.save()  
#     certificates = Certification.objects.filter(SellerProfile=seller)
#     videos = Video.objects.filter(SellerProfile=seller)
#     products = Product.objects.filter(SellerProfile=seller)

#     percentage_change = seller.calculate_percentage_change()

#     return render(request, 'companies/seller_detail.html', {
#         'seller': seller,
#         'certificates': certificates,
#         'videos': videos,
#         'products': products,
#         'percentage_change': percentage_change,
#         'socialmedia' : socialmedia,
#         'meta': meta,
#     })



def seller_detail(request,company_slug):
    meta = PageMeta.objects.filter(slug="seller_detail").first()
    socialmedia = SocialMediaLinks.objects.all()
    
    # seller = SellerProfile.objects.filter(
    #     company_name__iexact=company_name.replace('-', ' ')
    # ).first()
    # if not seller:
    #     raise Http404("Seller not found")
    seller = SellerProfile.objects.filter(slug=company_slug).first()
    if not seller:
        raise Http404("Seller not found")

    ProfileViewLog.objects.create(seller=seller)
    seller.update_views()
    
    if seller.profile_views > 50:
        seller.is_verified = True
    if seller.profile_views > 100:
        seller.is_gold = True
    seller.save()

    certificates = Certification.objects.filter(SellerProfile=seller)
    videos = Video.objects.filter(SellerProfile=seller)
    products = Product.objects.filter(SellerProfile=seller)
    percentage_change = seller.calculate_percentage_change()

    return render(request, 'companies/seller_detail.html', {
        'seller': seller,
        'certificates': certificates,
        'videos': videos,
        'products': products,
        'percentage_change': percentage_change,
        'socialmedia': socialmedia,
        'meta': meta,
    })






def seller_dashboard(request):
    meta = PageMeta.objects.filter(slug="seller_dashboard").first()
    if request.user.is_authenticated and hasattr(request.user, 'buyerprofile'):
        return redirect('log_reg')  

    if not request.user.is_authenticated:
        return redirect('company_login') 
    
    sellerprofile = SellerProfile.objects.filter(user=request.user).first()

    if not sellerprofile:
        return redirect('restriction')  
    

    percentage_change = sellerprofile.calculate_percentage_change()


    fields_of_work_choices = SellerProfile._meta.get_field('fields_of_work').choices
    certificates = Certification.objects.filter(SellerProfile=sellerprofile)
    videos = Video.objects.filter(SellerProfile=sellerprofile)
    products = Product.objects.filter(SellerProfile=sellerprofile)
    categories = Category.objects.all() 

    return render(request, 'companies/seller_dashboard.html', {
        'sellerprofile': sellerprofile,
        'fields_of_work_choices': fields_of_work_choices,
        'certificates': certificates,
        'videos': videos,
        'products': products,
        'profile_views': sellerprofile.profile_views,
        'daily_views': sellerprofile.daily_views,
        'weekly_views': sellerprofile.weekly_views,
        'percentage_change': percentage_change,
        'categories': categories,
        'meta': meta,
    })







def restriction(request):
    return render(request, 'companies/restriction.html')







def add_product(request):
    sellerprofile = SellerProfile.objects.filter(user=request.user).first()
    if not sellerprofile:
        return JsonResponse({'success': False, 'error': 'You need a seller profile to add products.'})

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        images = request.FILES.getlist('product_images')

        if form.is_valid():
            product = form.save(commit=False)
            product.SellerProfile = sellerprofile
            product.save()

            if images:
                for image in images:
                    ProductImage.objects.create(image=image, product=product)

            return JsonResponse({'success': True, 'message': 'Product added successfully!'})

        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})

    categories = Category.objects.all()
    return render(request, 'seller_dashboard.html', {'categories': categories})










def edit_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        name = request.POST.get('name')
        origin = request.POST.get('origin')
        availability = request.POST.get('availability')
        description = request.POST.get('description')  
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')

        product = get_object_or_404(Product, id=product_id, SellerProfile__user=request.user)

        product.name = name
        product.origin = origin
        product.availability = availability
        product.description = description  

        if category_id:
            product.category = get_object_or_404(Category, id=category_id)
        if subcategory_id:
            product.subcategory = get_object_or_404(SubCategory, id=subcategory_id)

        removed_images = request.POST.get('removed_images', '')
        if removed_images:
            removed_image_ids = [int(id) for id in removed_images.split(',') if id]
            ProductImage.objects.filter(id__in=removed_image_ids).delete()

        if 'product_images' in request.FILES:
            for image in request.FILES.getlist('product_images'):
                ProductImage.objects.create(product=product, image=image)

        product.save()
        messages.success(request, "Product updated successfully!")

        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request"})


def remove_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if product.SellerProfile.user == request.user:
        product.delete()
        messages.success(request, "Product removed successfully.")
    else:
        messages.error(request, "You are not authorized to remove this product.")
    return redirect('seller_dashboard')





def add_video(request):
    sellerprofile = SellerProfile.objects.filter(user=request.user).first()  
    if not sellerprofile:
        return redirect('some_error_page')  

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)  
        if form.is_valid():
            new_video = form.save(commit=False)
            new_video.SellerProfile = sellerprofile  
            new_video.save()
            messages.success(request, "Video added successfully!")
            return redirect('seller_dashboard') 
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    readable_field = field.replace('_', ' ').title()
                    error_messages.append(f"{readable_field}: {error}")
            messages.error(request, "There was an error. " + " | ".join(error_messages))

    else:
        form = VideoForm()

    return render(request, 'companies/seller_dashboard.html', {'form': form})



def remove_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    
    if video.SellerProfile.user == request.user:
        video.delete()
        messages.success(request, "Video removed successfully!")
    
    return redirect('seller_dashboard')





# def categories_processor(request):
#     categories = Category.objects.prefetch_related('subcategories')
#     return {'categories': categories}










def get_subcategories(request, category_id):
    try:
        subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
        return JsonResponse({'subcategories': list(subcategories)})
    except Category.DoesNotExist:
        return JsonResponse({'subcategories': []}, status=404)



def subcategory_products_view(request, subcategory_id=None , subcategory_name=None):
    meta = PageMeta.objects.filter(slug="subcategory_products_view").first()
    socialmedia = SocialMediaLinks.objects.all()
    category_filter = request.GET.get('category')
    subcategories = []

    if subcategory_id:
        subcategory = get_object_or_404(SubCategory, id=subcategory_id)
        category = subcategory.category
        products = Product.objects.filter(subcategory=subcategory)
    else:
        category_id = request.GET.get('category')
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
        subcategories = category.subcategories.all()
    category_filter = request.GET.get('category')
    if category_filter:
        products = Product.objects.filter(category_id=category_filter)

    subcategory_filter = request.GET.get('subcategory')
    if subcategory_filter:
        products = products.filter(subcategory_id=subcategory_filter)

    origin_filter = request.GET.get('origin')
    if origin_filter:
        products = products.filter(origin__icontains=origin_filter)

    availability_filter = request.GET.get('availability')
    if availability_filter:
        products = products.filter(availability=availability_filter)

    sort_by = request.GET.get('sort_by')
    if sort_by == 'newest':
        products = products.order_by('-id')
    elif sort_by == 'most_popular':
        products = products.order_by('-popularity')

    item_count = products.count()
    paginator = Paginator(products, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    query_params = request.GET.copy()
    query_params['page'] = None  
    base_url = request.path + '?' + query_params.urlencode()

    return render(request, 'first/subcategory_products.html', {
        'subcategory': subcategory if subcategory_id else SubCategory.objects.filter(id=request.GET.get('subcategory')).first(),
        # 'subcategory': subcategory if subcategory_id else None,
        'category': category,
        'products': products,
        'categories': Category.objects.all(),
        'subcategories': subcategories,  
        'products': page_obj, 
        'base_url': base_url,
        'socialmedia': socialmedia,
        'item_count': item_count,
        'meta': meta,
    })











def convert_pdf_to_images(instance):
    images = convert_from_path(instance.pdf_file.path)
    for i, img in enumerate(images):
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        filename = f"{instance.pk}_page_{i+1}.jpg"
        path = default_storage.save(f'catalogue_pages/{filename}', ContentFile(buffer.getvalue()))
        CataloguePagePdf.objects.create(
            catalogue=instance,
            page_number=i + 1,
            image=path
        )





def catalogue_list(request):
    meta = PageMeta.objects.filter(slug="catalogue_list").first()

    catalogues = CataloguePdf.objects.all()


    socialmedia = SocialMediaLinks.objects.all()
    sort_option = request.GET.get('sort', 'newest')  
    if sort_option == "most_downloaded":
        catalogues = CataloguePdf.objects.all().order_by('-download_count')
    elif sort_option == "most_viewed":
        catalogues = CataloguePdf.objects.all().order_by('-view_count')
    else:  
        catalogues = CataloguePdf.objects.all().order_by('-publish_date')

    total_catalogues = catalogues.count() 
    latest_catalogues = CataloguePdf.objects.all().order_by('-publish_date')[:3]
    return render(request, 'companies/catalogue_list.html', {'catalogues': catalogues, 'catalogues': catalogues,
        'total_catalogues': total_catalogues,
        'sort_option': sort_option,
        'socialmedia' : socialmedia,
        'latest_catalogues': latest_catalogues,
        'meta': meta,
        })

# def catalogue_detail(request, pk):
#     meta = PageMeta.objects.filter(slug="catalogue_detail").first()
#     catalogue = get_object_or_404(CataloguePdf, pk=pk)
#     socialmedia = SocialMediaLinks.objects.all()
#     return render(request, 'companies/catalogue_detail_list.html', {'catalogue': catalogue, 'socialmedia' : socialmedia,'meta': meta,})






# def catalogue_detail(request, pk):
#     meta = PageMeta.objects.filter(slug="catalogue_detail").first()
#     catalogue = get_object_or_404(CataloguePdf, pk=pk)
#     socialmedia = SocialMediaLinks.objects.all()

#     comments = catalogue.comments.select_related('user').order_by('-created_at')
#     for comment in comments:
#         try:
#             comment.rating = int(comment.rating)
#         except (ValueError, TypeError):
#             comment.rating = 0
#     form = None

#     if request.user.is_authenticated and request.user.user_type == 'buyer':
#         if request.method == 'POST':
#             form = CatalogueCommentForm(request.POST)
#             if form.is_valid():
#                 new_comment = form.save(commit=False)
#                 new_comment.catalogue = catalogue
#                 new_comment.user = request.user
#                 new_comment.save()
#                 messages.success(request, 'Comment submitted successfully.')
#                 return redirect('catalogue_detail', pk=pk)
#         else:
#             form = CatalogueCommentForm()

#     return render(request, 'companies/catalogue_detail_list.html', {
#         'catalogue': catalogue,
#         'socialmedia': socialmedia,
#         'meta': meta,
#         'comments': comments,
#         'form': form,
#     })



def catalogue_detail(request, pk):
    meta = PageMeta.objects.filter(slug="catalogue_detail").first()
    catalogue = get_object_or_404(CataloguePdf, pk=pk)
    socialmedia = SocialMediaLinks.objects.all()

    comments = catalogue.comments.select_related('user').order_by('-created_at')

    if comments.exists():
        average_rating = sum(comment.rating for comment in comments) / comments.count()
    else:
        average_rating = 0

    form = None

    if request.user.is_authenticated and request.user.user_type == 'buyer':
        if request.method == 'POST':
            form = CatalogueCommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.catalogue = catalogue
                new_comment.user = request.user
                new_comment.save()
                messages.success(request, 'Comment submitted successfully.')
                return redirect('catalogue_detail', pk=pk)
        else:
            form = CatalogueCommentForm()

    return render(request, 'companies/catalogue_detail_list.html', {
        'catalogue': catalogue,
        'socialmedia': socialmedia,
        'meta': meta,
        'comments': comments,
        'form': form,
        'average_rating': average_rating,
        'star_range': range(1, 6),  
    })





def catalogue_page_detail(request, pk):
    meta = PageMeta.objects.filter(slug="catalogue_page_detail").first()
    page = get_object_or_404(CataloguePagePdf, pk=pk)
    catalogue = page.catalogue
    socialmedia = SocialMediaLinks.objects.all()
    return render(request, 'companies/catalogue_page_detail_list.html', {'page': page,'socialmedia' : socialmedia,'catalogue': catalogue,'meta': meta,})




def increment_download_count(request, catalogue_id):
    CataloguePdf.objects.filter(id=catalogue_id).update(download_count=F('download_count') + 1)
    updated_count = CataloguePdf.objects.get(id=catalogue_id).download_count
    return JsonResponse({'success': True, 'new_count': updated_count})


def download_catalogue(request, catalogue_id):
    catalogue = get_object_or_404(CataloguePdf, id=catalogue_id)
    pages = catalogue.pagesss.all()  

    if not pages.exists():
        raise Http404("No pages found for this catalogue.")

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    for page in pages:
        if page.image:  
            image_path = os.path.join(settings.MEDIA_ROOT, str(page.image))
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img_width, img_height = img.size
                a4_width, a4_height = A4
                aspect_ratio = img_width / img_height
                new_width = a4_width
                new_height = new_width / aspect_ratio
                if new_height > a4_height:
                    new_height = a4_height
                    new_width = new_height * aspect_ratio
                x = (a4_width - new_width) / 2
                y = (a4_height - new_height) / 2
                pdf.drawImage(image_path, x, y, width=new_width, height=new_height)
                pdf.showPage()

    pdf.save()
    buffer.seek(0)
    filename = f"{catalogue.creator}-catalogue.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)






def increase_catalogue_view(request, catalogue_id):
    catalogue = get_object_or_404(CataloguePdf, id=catalogue_id)
    catalogue.view_count += 1
    catalogue.save()
    return JsonResponse({"view_count": catalogue.view_count})
