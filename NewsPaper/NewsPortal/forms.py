from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from .models import Post


class NewsForm(forms.ModelForm):
    content = forms.CharField(min_length=10)

    class Meta:
        model = Post
        fields = ['header',
                  'author',
                  'content',
                  'category',
                  ]

        def clean(self):
            cleaned_data = super().clean()
            content = cleaned_data.get("content")
            header = cleaned_data.get('header')

            if header == content:
                raise ValidationError(
                    "Заголовок не может быть идентичен названию"
                )

            return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
