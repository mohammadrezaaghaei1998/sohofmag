from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import CustomUser
from .models import BuyerProfile
from captcha.fields import CaptchaField





# class BuyerSignupForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'password1', 'password2']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.user_type = "buyer"

#         if not user.username:
#             user.username = user.email 

            
#         if commit:
#             user.save()
#             BuyerProfile.objects.create(user=user)
#         return user




# class BuyerLoginForm(AuthenticationForm):
#     email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email address'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
#     captcha = CaptchaField()

#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data.get('email')
#         password = cleaned_data.get('password')

#         if email and password:
#             try:
#                 user = CustomUser.objects.get(email=email)
#                 if not user.check_password(password): 
#                     raise forms.ValidationError("Invalid username or password.")
#             except CustomUser.DoesNotExist:
#                 raise forms.ValidationError("Invalid username or password.")
#         return cleaned_data
    

class BuyerSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "buyer"
        if commit:
            user.save()
            BuyerProfile.objects.create(user=user)
        return user



class BuyerLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    captcha = CaptchaField()

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = CustomUser.objects.get(username=username)
                if not user.check_password(password):
                    raise forms.ValidationError("Invalid username or password.")
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Invalid username or password.")

        if 'captcha' in self.errors:
            raise forms.ValidationError("Invalid captcha.")
        return cleaned_data







class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        fields = ['name', 'last_name', 'address', 'phone', 'tax_number', 'postal_code', 'image']

    username = forms.CharField(max_length=150)
    email = forms.EmailField()


    


# class BuyerProfileForm(forms.ModelForm):
#     class Meta:
#         model = BuyerProfile
#         fields = ['name','last_name',  'address', 'phone', 'tax_number', 'postal_code','image']
