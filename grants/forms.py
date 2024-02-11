from django.forms import ModelForm

from projects.models import GrantModel, SponsoredMoneyModel


class NewGrantForm(ModelForm):
    class Meta:
        model = GrantModel
        fields = ['name']


class NewSponsoredMoneyForm(ModelForm):
    class Meta:
        model = SponsoredMoneyModel
        fields = ['project',
                  'money', ]

