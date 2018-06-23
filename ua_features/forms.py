from django import forms
from .models import UaFeature, Post


class UaFeatureForm(forms.ModelForm):
    name = forms.CharField(label="Feature name")
    is_a_poll = forms.BooleanField(label=('Include a poll?'),
                                   widget=forms.HiddenInput(), required=False, initial=True)

    class Meta:
        model = UaFeature
        fields = ['name']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['comment']
