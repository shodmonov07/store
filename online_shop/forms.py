from django import forms
from django.contrib.auth.models import User

from online_shop.models import Comment, Order, Product


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = ['name','email','body']
        exclude = ('product',)

    def clean_email(self):
        email = self.data.get('email')
        if Comment.objects.filter(email=email).exists():
            raise forms.ValidationError(f'This {email} is already used')
        return email


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('product',)


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_username(self):
        username = self.data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'This {username} is already exists')
        return username

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data['password']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True

        if commit:
            user.save()

        return user