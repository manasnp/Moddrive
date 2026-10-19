from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date
from .models import UserProfile

class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    birthdate = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1900, 2027)),
    )

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get("birthdate")
        today = date.today()

        if not birthdate:
             raise forms.ValidationError("Birthdate is required.")

        if birthdate > today:
                    raise forms.ValidationError("Birthdate cannot be in the future.")
        
        age = today.year - birthdate.year
        if (today.month, today.day)<(birthdate.month, birthdate.day): 
            age -= 1
        
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        return birthdate

    class Meta:
        model = User
        fields = ("full_name", "username", "email", "birthdate", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        full_name = self.cleaned_data ['full_name']
        name_parts = full_name.strip().split(maxsplit=1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ""
        if commit:
            user.save()
            # Create a UserProfile instance for the new user
            UserProfile.objects.create(user=user, birthdate=self.cleaned_data['birthdate'])
        return user

    # email uniqueness validation

    def clean_email(self):
         email = self.cleaned_data.get('email')

         if not email:
              raise forms.ValidationError("Email is required.")

         email = email.strip().lower() # Normalize the email address
            
         if User.objects.filter(email__iexact=email).exists():
              raise forms.ValidationError("This email address is already in use. Please use a different email address.")
         return email

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")

        if not full_name:
            raise forms.ValidationError("Full name is required.")

        full_name = full_name.strip()
        name_parts = full_name.split(maxsplit=1)

        if len(name_parts) < 2:
            raise forms.ValidationError(
                "Please enter both first and last names."
            )

        return full_name

  
