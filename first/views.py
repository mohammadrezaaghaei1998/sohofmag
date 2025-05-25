from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import BuyerLoginForm, BuyerSignupForm 
from accounts.models import CustomUser
from django.contrib import messages
from companies.models import Product,Product, SellerProfile,SubCategory,CataloguePdf
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import BuyerProfile , Wishlist,Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from about_us.models import (AboutUsVideo, HomePageVideo,
    AboutUsVideo, AboutUsImageTitle,AboutUsImages,AboutUsMainTitle,AboutUsFounder,AboutUsOurVision,AboutUsQualityObjectives,AboutUsKeyStrategies,
    AboutUsOurPolicy,AboutUsOurPolicyBox,AboutUsOurPolicyItems,TabSection,TabItem,HistoryItem,OurTeam,Partner)
from companies .models import Category
from socialmedia.models import SocialMediaLinks
from django.contrib.auth.decorators import login_required
from .forms import  BuyerProfileForm
from advertising.models import Advertisement
from contact.models import ContactUsHeader,ContactInfo,FAQ
from homepage.models import (CarouselSlide,WhatWeDoCard, WhatWeDoSection, CategoryHighlightSection,
                              CategoryHighlightBox,CatalogueHighlightSection,FifthSection,SixthSection,SeventhSection,EighthSection)

from metatags.models import PageMeta
from django.db.models import Q
from django.utils.text import slugify


def index(request):
    meta = PageMeta.objects.filter(slug="homepage").first()
    socialmedia = SocialMediaLinks.objects.all()
    catalogues = CataloguePdf.objects.all()
    categories = Category.objects.all()
    homepagevideos = HomePageVideo.objects.all()
    advertisement = Advertisement.objects.all()
    carouselslides = CarouselSlide.objects.all()
    whatwedo_cards = WhatWeDoCard.objects.all()
    whatwedo_section = WhatWeDoSection.objects.first()
    category_highlight = CategoryHighlightSection.objects.prefetch_related('boxes').first()
    catalogue_highlight = CatalogueHighlightSection.objects.first()
    fifth_section = FifthSection.objects.first()
    sixth_section = SixthSection.objects.first()
    seventh_section = SeventhSection.objects.first()
    eighth_section = EighthSection.objects.first()

    return render(request, 'first/index.html', {
        'catalogues': catalogues,
        'categories': categories,
        'socialmedia': socialmedia,
        'homepagevideos': homepagevideos,
        'advertisement': advertisement,
        'carouselslides': carouselslides,
        'whatwedo_cards': whatwedo_cards,
        'whatwedo_section': whatwedo_section,
        'category_highlight': category_highlight,
        'catalogue_highlight': catalogue_highlight,
        'fifth_section': fifth_section,
        'sixth_section': sixth_section,
        'seventh_section': seventh_section,
        'eighth_section': eighth_section,
        'meta': meta,
    })



def aboutus(request):
    meta = PageMeta.objects.filter(slug="aboutus").first()
    socialmedia = SocialMediaLinks.objects.all()
    aboutusvideos = AboutUsVideo.objects.all()
    aboutus_image_titles = AboutUsImageTitle.objects.all()
    aboutus_images = AboutUsImages.objects.all()
    aboutus_main_titles = AboutUsMainTitle.objects.all()
    aboutus_founders = AboutUsFounder.objects.all()
    aboutus_our_visions = AboutUsOurVision.objects.all()
    aboutus_quality_objectives = AboutUsQualityObjectives.objects.all()
    aboutus_key_strategies = AboutUsKeyStrategies.objects.all()
    aboutus_our_policies = AboutUsOurPolicy.objects.all()
    aboutus_our_policy_boxes = AboutUsOurPolicyBox.objects.all()
    aboutus_our_policy_items = AboutUsOurPolicyItems.objects.all()
    tab_sections = TabSection.objects.all()
    tab_items = TabItem.objects.all()
    history_items = HistoryItem.objects.all()
    our_team = OurTeam.objects.all()
    partners = Partner.objects.all()

    return render(request, 'first/aboutus.html', {
        'socialmedia': socialmedia,
        'aboutusvideos': aboutusvideos,
        'aboutus_image_titles': aboutus_image_titles,
        'aboutus_images': aboutus_images,
        'aboutus_main_titles': aboutus_main_titles,
        'aboutus_founders': aboutus_founders,
        'aboutus_our_visions': aboutus_our_visions,
        'aboutus_quality_objectives': aboutus_quality_objectives,
        'aboutus_key_strategies': aboutus_key_strategies,
        'aboutus_our_policies': aboutus_our_policies,
        'aboutus_our_policy_boxes': aboutus_our_policy_boxes,
        'aboutus_our_policy_items': aboutus_our_policy_items,
        'tab_sections': tab_sections,
        'tab_items': tab_items,
        'history_items': history_items,
        'our_team': our_team,
        'partners': partners,
        'meta': meta,
    })



def contactus(request):
    meta = PageMeta.objects.filter(slug="contactus").first()
    socialmedia = SocialMediaLinks.objects.all()
    contact_us_header = ContactUsHeader.objects.first() 
    contact_info = ContactInfo.objects.first() 
    faqs = FAQ.objects.all()  

    return render(request, 'first/contactus.html', {
        'socialmedia': socialmedia,
        'contact_us_header': contact_us_header,
        'contact_info': contact_info,
        'faqs': faqs,  
        'meta': meta,
    })






def products(request):
    meta = PageMeta.objects.filter(slug="products").first()
    socialmedia = SocialMediaLinks.objects.all()
    products = Product.objects.all()
    products_list = Product.objects.all()  

    
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    origin_filter = request.GET.get('origin')
    availability_filter = request.GET.get('availability')
    sort_by = request.GET.get('sort_by')

    category = None
    subcategory = None
    subcategories = []
    latest_products = Product.objects.all().order_by('-id')[:4]
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category_id=category_id)
        subcategories = category.subcategories.all()  

    if subcategory_id:
        subcategory = get_object_or_404(SubCategory, id=subcategory_id)
        products = products.filter(subcategory_id=subcategory_id)

    if origin_filter:
        products = products.filter(origin__icontains=origin_filter)

    if availability_filter:
        products = products.filter(availability=availability_filter)

    
    if sort_by == 'newest':
        products = products.order_by('-id')
    elif sort_by == 'most_popular':
        products = products.order_by('-popularity')

    
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    base_url = request.path + '?' + query_params.urlencode()

    return render(request, 'first/products.html', {
        'products': page_obj,
        'category': category,
        'subcategory': subcategory,
        'categories': Category.objects.all(),
        'subcategories': subcategories,
        'socialmedia': socialmedia,
        'total_products': products.count(),
        'base_url': base_url,
        'meta': meta,
        'latest_products': latest_products,
    })






# def product_detail(request, product_id, product_name):
#     meta = PageMeta.objects.filter(slug="product_detail").first()
#     socialmedia = SocialMediaLinks.objects.all()
#     product = get_object_or_404(Product, id=product_id)
#     seller = product.SellerProfile

#     product_slug = slugify(product.name)
#     if product_name != product_slug:
#         return redirect('product_detail', product_id=product.id, product_name=product_slug)

#     similar_products = Product.objects.filter(
#         Q(category=product.category)  
#     ).exclude(id=product.id)  

#     if not similar_products.exists():
#         similar_products = Product.objects.all().exclude(id=product.id)[:10]  

#     return render(request, 'first/product_detail.html', {
#         'product': product,
#         'seller': seller,
#         'socialmedia': socialmedia,
#         'meta': meta,
#         'similar_products': similar_products,
#     })






def product_detail(request, product_id, product_name):
    meta = PageMeta.objects.filter(slug="product_detail").first()
    socialmedia = SocialMediaLinks.objects.all()
    product = get_object_or_404(Product, id=product_id)
    seller = product.SellerProfile

    product_slug = slugify(product.name)
    if product_name != product_slug:
        return redirect('product_detail', product_id=product.id, product_name=product_slug)

    name_keywords = product.name.split() if product.name else []

    name_query = Q()
    for word in name_keywords:
        name_query |= Q(name__icontains=word)

    similar_products = Product.objects.filter(name_query).exclude(id=product.id)

    if not similar_products.exists():
        similar_products = Product.objects.exclude(id=product.id)[:10]

    return render(request, 'first/product_detail.html', {
        'product': product,
        'seller': seller,
        'socialmedia': socialmedia,
        'meta': meta,
        'similar_products': similar_products,
    })









def log_reg(request):
    meta = PageMeta.objects.filter(slug="user_login").first()
    if request.user.is_authenticated and request.user.user_type == "seller":
        logout(request)
        return redirect('restrictions')

    login_form = BuyerLoginForm()
    signup_form = BuyerSignupForm()
    
    if request.method == "POST":
        if 'login' in request.POST:
            login_form = BuyerLoginForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user and user.user_type == "buyer":
                    login(request, user)
                    messages.success(request, "Login successful!")

                    next_url = request.GET.get("next") or request.POST.get("next")
                    return redirect(next_url or "index")
                    # return redirect("index")
                else:
                    messages.error(request, "Invalid credentials for a buyer account.")

            else:
                for field, error_list in login_form.errors.items():
                    for error in error_list:
                        messages.error(request, f"{field.capitalize()}: {error}")
                return redirect("log_reg")

        elif 'signup' in request.POST:
            signup_form = BuyerSignupForm(request.POST)
            if signup_form.is_valid():
                email = signup_form.cleaned_data.get('email')
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "This email is already registered.")
                else:
                    signup_form.save()
                    messages.success(request, "Signup successful! Please login.")
                    return redirect("log_reg")
            else:
                for field, error_list in signup_form.errors.items():
                    for error in error_list:
                        messages.error(request, f"{field.capitalize()}: {error}")
                return redirect("log_reg")

    context = {
        'form': login_form,
        'signup_form': signup_form,
        'meta': meta
    }
    return render(request, 'first/log_reg.html', context)









@login_required
def change_password(request):
    if request.user.user_type != 'buyer':
        messages.error(request, 'You do not have permission to change the password.')
        return redirect('user_dashboard') 

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)  

        if form.is_valid():
            if form.cleaned_data['new_password1'] == form.cleaned_data['old_password']:
                form.add_error('new_password1', 'New password cannot be the same as the old password.')
            else:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('user_dashboard')
        
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

        if form.errors.get('old_password'):
            messages.error(request, 'The old password you entered is incorrect.')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'first/user_dashboard.html', {'form': form})








def restrictions(request):
    socialmedia = SocialMediaLinks.objects.all()
    return render(request, 'first/restrictions.html',{ 'socialmedia' : socialmedia})





def user_dashboard(request):
    meta = PageMeta.objects.filter(slug="user_dashboard").first()
    socialmedia = SocialMediaLinks.objects.all()
    if not request.user.is_authenticated:
        return redirect('log_reg')  

    if hasattr(request.user, 'sellerprofile'):
        return redirect('company_login')  

    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product', 'product__SellerProfile')

    try:
        user_profile = BuyerProfile.objects.get(user=request.user)
    except BuyerProfile.DoesNotExist:
        user_profile = BuyerProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = BuyerProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Update CustomUser fields
            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']
            request.user.save()

            # Save the profile
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('user_dashboard')
    else:
        form = BuyerProfileForm(instance=user_profile)

    products = [item.product for item in wishlist_items]
    return render(request, 'first/user_dashboard.html', {
        'user_profile': user_profile,
        'form': form,
        'wishlist_items': wishlist_items,
        'products': products,
        'socialmedia' : socialmedia,
        'meta': meta,
    })



def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("index") 






# @csrf_exempt
# @login_required
# def add_to_wishlist(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
        
#         try:
#             product = Product.objects.get(id=product_id)
#             wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
            
#             print(f'Product {product.name} added to wishlist.')  
            
#             if created:
#                 return JsonResponse({'success': True, 'message': 'Product added to wishlist.'})
#             else:
#                 return JsonResponse({'success': False, 'message': 'Product is already in your wishlist.'})
#         except Product.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'Product not found.'})

#     return JsonResponse({'success': False, 'message': 'Invalid request.'})




@csrf_exempt
@login_required
def add_to_wishlist(request):
    if request.method == 'POST':
        if request.user.user_type != 'buyer':
            return JsonResponse({'success': False, 'message': 'This feature is not available for your account type.'})

        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
            
            if created:
                return JsonResponse({'success': True, 'message': 'Product added to wishlist.'})
            else:
                return JsonResponse({'success': False, 'message': 'Product is already in your wishlist.'})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})





@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    products_in_wishlist = [item.product for item in wishlist_items]


    
    return render(request, 'user_dashboard.html', {'products_in_wishlist': products_in_wishlist})





@csrf_exempt
@login_required
def remove_from_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        try:
            wishlist_item = Wishlist.objects.get(user=request.user, product_id=product_id)
            wishlist_item.delete()
            return JsonResponse({'success': True, 'message': 'Removed from wishlist.'})
        except Wishlist.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found in wishlist.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})





def search_view(request):
    meta = PageMeta.objects.filter(slug="search_view").first()
    query = request.GET.get('q', '')
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category_id=category_filter)

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

    categories = Category.objects.all()

    selected_category_id = request.GET.get('category')
    selected_subcategory_id = request.GET.get('subcategory')

    if not selected_category_id and products.exists():
        selected_category_id = products.first().category_id

    if not selected_subcategory_id and products.exists():
        selected_subcategory_id = products.first().subcategory_id

    if selected_category_id:
        subcategories = SubCategory.objects.filter(category_id=selected_category_id)
    else:
        subcategories = SubCategory.objects.none()

    return render(request, 'first/search_result.html', {
        'query': query,
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
        'selected_category_id': str(selected_category_id) if selected_category_id else '',
        'selected_subcategory_id': str(selected_subcategory_id) if selected_subcategory_id else '',
        'meta': meta,
    })


