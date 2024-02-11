from django.forms import ModelForm

from projects.models import TeamModel


class NewTeamForm(ModelForm):
    class Meta:
        model = TeamModel
        fields = [
            'name',
            'vk_link',
            'manager',
            'person_from_gov',
            'person_from_company',
            'found_date',
        ]
