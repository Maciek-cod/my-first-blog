from django import forms
from .models import Listing, Bid, Comment


class ItemForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('title', 'description','start_bit','picture_URL','category')
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'description': forms.TextInput(attrs={'class': 'form-control'}),
                   'picture_URL': forms.URLInput(attrs={'class': 'form-control'}),
                   'category': forms.Select(attrs={'class': 'form-control'}),
                   'start_bit': forms.NumberInput(attrs={'class': 'form-control'})} 


class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ('bid',)
        widgets = {'bid': forms.TextInput(attrs={'class': 'form-control'})}


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {'comment': forms.TextInput(attrs={'class': 'form-control'})}