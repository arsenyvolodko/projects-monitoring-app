from django.forms import ModelForm, inlineformset_factory
from django import forms

from projects.models import TeamModel, MemberModel


class NewMemberForm(ModelForm):
    class Meta:
        model = MemberModel
        fields = [
            'first_name',
            'second_name',
            'last_name',
            'status',
            'team',
            'email',
            'phone',
            'tg_username',
            'date_of_birth',
            'city',
            'school',
            'grade',
            'languages',
            'subjects',
            'skills',
            'hobbies',
            'achievements',
            'more_info',
        ]
