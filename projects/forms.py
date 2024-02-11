from django.forms import ModelForm, Select

from projects.models import ProjectModel, SponsoredMoneyModel


class NewProjectForm(ModelForm):
    class Meta:
        model = ProjectModel
        fields = ['name', 'description', 'by_team', 'manager', 'author', 'period_type', 'start_date', 'end_date',
                  'status']
        widgets = {
            'period_type': Select(choices=ProjectModel.PERIOD_TYPE_CHOICES),
        }


class NewSponsoredMoneyForm(ModelForm):
    class Meta:
        model = SponsoredMoneyModel
        fields = ['grant',
                  'money', ]
