from django import forms

from online_shop.models import Comment, Order


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
