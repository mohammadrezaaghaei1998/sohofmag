from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import CustomUser
from .models import SellerProfile, Certification, Video, Product, ProductImage,SubCategory,CatalogueComment
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from django.utils.text import slugify
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re



class SellerSignupForm(UserCreationForm):
    
    company_name = forms.CharField(required=True)
    company_address = forms.CharField(widget=forms.Textarea, required=True)
    website_url = forms.URLField(required=True)
    fields_of_work = forms.ChoiceField(choices=SellerProfile._meta.get_field('fields_of_work').choices, required=True)
    company_description = forms.CharField(widget=forms.Textarea, required=True)
    company_location = forms.CharField(required=True)
    year_established = forms.IntegerField(required=True)
    company_size = forms.IntegerField(required=False)
    contact_email = forms.EmailField(required=True)
    company_logo = forms.ImageField(required=False)

    
    full_name = forms.CharField(required=True)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=True)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=True)
    phone_number = forms.CharField(required=True)
    email_address = forms.EmailField(required=True)
    country = forms.CharField(required=True)

    
    accepted_terms = forms.BooleanField(required=True, label="I accept the terms and conditions")

   
    username = forms.CharField(required=True, max_length=150)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)

       
        user.email = self.cleaned_data['email_address'] 
        user.user_type = "seller"

        if commit:
            user.save()
            slug = slugify(self.cleaned_data['company_name'])

            SellerProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                company_address=self.cleaned_data['company_address'],
                website_url=self.cleaned_data['website_url'],
                fields_of_work=self.cleaned_data['fields_of_work'],
                company_description=self.cleaned_data['company_description'],
                company_location=self.cleaned_data['company_location'],
                year_established=self.cleaned_data['year_established'],
                company_size=self.cleaned_data['company_size'],
                contact_email=self.cleaned_data['contact_email'],
                company_logo=self.cleaned_data.get('company_logo'),
                full_name=self.cleaned_data['full_name'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                phone_number=self.cleaned_data['phone_number'],
                email_address=self.cleaned_data['email_address'],
                address=self.cleaned_data['address'],
                country=self.cleaned_data['country'],
                company_license=self.cleaned_data['company_license'],
                id_card=self.cleaned_data.get('id_card'),
                passport=self.cleaned_data.get('passport'),
                certificates=self.cleaned_data.get('certificates'),
                tax_registration=self.cleaned_data.get('tax_registration'),
                utility_bill=self.cleaned_data.get('utility_bill'),
                bank_statement=self.cleaned_data.get('bank_statement'),
                accepted_terms=self.cleaned_data['accepted_terms'],
                slug=slug,
            )
        return user



class SellerLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    captcha = CaptchaField()
    





SAFE_DOMAINS = [
    'facebook.com',
    'instagram.com',
    'linkedin.com',
    'twitter.com',
    'youtube.com',
]

def validate_safe_social_url(value):
    validator = URLValidator()
    try:
        validator(value)
    except ValidationError:
        raise ValidationError("Invalid URL format.")
    
    if not any(domain in value for domain in SAFE_DOMAINS):
        raise ValidationError("Only official social media URLs are allowed.")

class SellerProfileUpdateForm(forms.ModelForm):
    instagram = forms.URLField(required=False, validators=[validate_safe_social_url])
    facebook = forms.URLField(required=False, validators=[validate_safe_social_url])
    twitter = forms.URLField(required=False, validators=[validate_safe_social_url])
    linkedin = forms.URLField(required=False, validators=[validate_safe_social_url])
    youtube = forms.URLField(required=False, validators=[validate_safe_social_url])

    class Meta:
        model = SellerProfile
        exclude = ['company_logo', 'company_license', 'tax_registration', 'utility_bill',
                    'bank_statement', 'user', 'company_address', 'full_name',
                      'date_of_birth', 'gender', 'phone_number', 'email_address', 'address', 'country','profile_views', 'daily_views', 'weekly_views'
                  ]



class SellerProfileDocumentUpdateForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['company_logo', 'company_license', 'tax_registration', 'utility_bill', 'bank_statement','id_card','passport']


    def clean_company_logo(self):
        logo = self.cleaned_data.get('company_logo')
        if logo:
           
            if logo.size > 10 * 1024 * 1024:  
                raise ValidationError('The logo file size should not exceed 10MB.')
            
            if not logo.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError('Only image files are allowed for the logo.')
        return logo

    def clean_company_license(self):
        license_file = self.cleaned_data.get('company_license')
        if license_file:
            
            if license_file.size > 10 * 1024 * 1024: 
                raise ValidationError('The company license file size should not exceed 10MB.')
            
            if not license_file.name.lower().endswith('.pdf'):
                raise ValidationError('Only PDF files are allowed for the company license.')
        return license_file

    def clean_tax_registration(self):
        tax_registration = self.cleaned_data.get('tax_registration')
        if tax_registration:
            
            if tax_registration.size > 10 * 1024 * 1024:  
                raise ValidationError('The tax registration file size should not exceed 10MB.')
            
            if not tax_registration.name.lower().endswith('.pdf'):
                raise ValidationError('Only PDF files are allowed for the tax registration.')
        return tax_registration

    def clean_utility_bill(self):
        utility_bill = self.cleaned_data.get('utility_bill')
        if utility_bill:
           
            if utility_bill.size > 10 * 1024 * 1024:  
                raise ValidationError('The utility bill file size should not exceed 10MB.')
            
            if not utility_bill.name.lower().endswith('.pdf'):
                raise ValidationError('Only PDF files are allowed for the utility bill.')
        return utility_bill

    def clean_bank_statement(self):
        bank_statement = self.cleaned_data.get('bank_statement')
        if bank_statement:
            
            if bank_statement.size > 10 * 1024 * 1024: 
                raise ValidationError('The bank statement file size should not exceed 10MB.')
            
            if not bank_statement.name.lower().endswith('.pdf'):
                raise ValidationError('Only PDF files are allowed for the bank statement.')
        return bank_statement

    def clean_id_card(self):
        id_card = self.cleaned_data.get('id_card')
        if id_card:
            
            if id_card.size > 10 * 1024 * 1024: 
                raise ValidationError('The ID card file size should not exceed 10MB.')
           
            if not id_card.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError('Only image files are allowed for the ID card.')
        return id_card

    def clean_passport(self):
        passport = self.cleaned_data.get('passport')
        if passport:
            
            if passport.size > 10 * 1024 * 1024: 
                raise ValidationError('The passport file size should not exceed 10MB.')
           
            if not passport.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError('Only image files are allowed for the passport.')
        return passport





class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['title', 'description', 'image']


    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
           
            max_size = 10 * 1024 * 1024
            if image.size > max_size:
                raise ValidationError("File size should not exceed 10MB.")

          
            valid_mime_types = ['image/jpeg', 'image/png', 'image/gif']
            if image.content_type not in valid_mime_types:
                raise ValidationError("Only JPEG, PNG, or GIF images are allowed.")
            
        return image



class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_file']

    def clean_video_file(self):
        video = self.cleaned_data.get('video_file')

       
        max_size = 50 * 1024 * 1024 
        if video.size > max_size:
            raise ValidationError("The video file is too large. The maximum allowed size is 50 MB.")

       
        valid_formats = ['video/mp4', 'video/x-msvideo', 'video/x-matroska']
        if video.content_type not in valid_formats:
            raise ValidationError("Invalid video format. Please upload an mp4, avi, or mkv file.")

        return video




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'origin', 'description', 'availability', 'category', 'subcategory']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass 
        else:
            self.fields['subcategory'].queryset = SubCategory.objects.none()



class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']







 

# class CatalogueCommentForm(forms.ModelForm):
#     class Meta:
#         model = CatalogueComment
#         fields = ['comment', 'rating']
#         widgets = {
#             'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'}),
#             'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
#         }



class CatalogueCommentForm(forms.ModelForm):
    class Meta:
        model = CatalogueComment
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment...',
                'class': 'form-control w-100'  
            }),
            'rating': forms.RadioSelect(choices=[
                (5, '★'), (4, '★'), (3, '★'), (2, '★'), (1, '★')
            ]),
        }