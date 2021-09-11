from django import forms

from core.forms import BootstrapFormMixin
from petstagram.common.models import Comment
from petstagram.pets.models import Pet


class PetForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Pet
        exclude = ['user',]


class CommentPetForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', ]
