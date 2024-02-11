from django.db import models
from django.db.models import Sum


# from projects.models import ProjectModel

class TeamModel(models.Model):
    name = models.CharField()
    vk_link = models.URLField(blank=True, null=True)
    person_from_gov = models.CharField(blank=True, null=True)
    person_from_company = models.CharField(blank=True, null=True)
    found_date = models.DateField(blank=True, null=True)
    manager = models.CharField(blank=True, null=True)

    def get_member_num(self):
        return MemberModel.objects.filter(team__name=self.name).count()

    def get_members(self):
        return MemberModel.objects.filter(team__name=self.name)

    def get_running_projects(self):
        return ProjectModel.objects.filter(by_team__name=self.name)

    def __str__(self):
        return self.name


class ProjectModel(models.Model):
    PERIOD_TYPE_CHOICES = [
        ('долгосрочный', 'долгосрочный'),
        ('краткосрочный', 'краткосрочный'),
    ]

    name = models.CharField(unique=True)
    description = models.CharField()
    by_team = models.ForeignKey(TeamModel, on_delete=models.PROTECT)
    manager = models.CharField(blank=True, null=True)
    author = models.CharField(blank=True, null=True)
    period_type = models.CharField(max_length=20, choices=PERIOD_TYPE_CHOICES)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=False)

    def get_fields(self):
        return [i for i in self._meta.fields]

    def get_fields_strings(self):
        return {
            'name': "Название проекта",
            'description': "Описание проекта",
            'by_team': "Совет-реализатор",
            'manager': "Автор проекта",
            'period_type': "Долгосрочный/краткосрочный",
            'start_date': "Дата реализации",
            'end_date': "Дата завершения",
        }

    def __str__(self):
        return self.name

    def get_sponsored_money(self):
        # if grant_name:
        #     res = SponsoredMoneyModel.objects.filter(project__name=self.name, grant__name=grant_name).aggregate(Sum('money')).get('money__sum', 0)
        # else:
        res = SponsoredMoneyModel.objects.filter(project__name=self.name).aggregate(Sum('money')).get('money__sum', 0.0)
        return res if res is not None else 0.0

    def get_sponsored_money_from_specific_grant(self, grant_name):
        res = SponsoredMoneyModel.objects.filter(project__name=self.name, grant__name=grant_name).aggregate(
            Sum('money')).get('money__sum', 0.0)
        return res if res is not None else "не подавали"

    def get_sponsored_money_from_all_grants(self):
        grants = GrantModel.objects.all()
        return {grant: self.get_sponsored_money_from_specific_grant(grant.name) for grant in grants}


class GrantModel(models.Model):
    name = models.CharField(unique=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_grants():
        return GrantModel.objects.all()

    @staticmethod
    def get_all_sponsored_money():
        res = SponsoredMoneyModel.objects.all().aggregate(Sum('money')).get('money__sum', 0.0)
        return res if res is not None else 0.0

    def get_sponsored_money(self):
        res = SponsoredMoneyModel.objects.filter(grant__name=self.name).aggregate(Sum('money')).get('money__sum', 0.0)
        return res if res is not None else 0.0

    def get_sponsored_money_for_specific_project(self, project_name):
        res = SponsoredMoneyModel.objects.filter(project__name=project_name, grant__name=self.name).aggregate(
            Sum('money')).get('money__sum', 0.0)
        return res if res is not None else "не подавали"

    def get_sponsored_money_for_all_projects(self):
        projects = ProjectModel.objects.all()
        return {project.name: self.get_sponsored_money_for_specific_project(project.name) for project in projects}

    def get_only_involved_projects(self):
        projects = ProjectModel.objects.all()
        res = {}
        for project in projects:
            val = self.get_sponsored_money_for_specific_project(project.name)
            if val != 'не подавали':
                res[project] = val
        return res


class SponsoredMoneyModel(models.Model):
    project = models.ForeignKey(ProjectModel, on_delete=models.PROTECT)
    money = models.FloatField()
    grant = models.ForeignKey(GrantModel, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.project.name} - {self.grant.name} - {self.money}'

    @staticmethod
    def get_model_by_project_and_grant(project_id, grant_id):
        return SponsoredMoneyModel.objects.filter(project__id=project_id, grant__id=grant_id)


MEMBER_STATUS_CHOICES = [
    ('школьник', 'школьник'),
    ('студент', 'студент'),
]

MEMBER_GRADE_CHOICES = [
    ('7 класс', '7 класс'),
    ('8 класс', '8 класс'),
    ('9 класс', '9 класс'),
    ('10 класс', '10 класс'),
    ('11 класс', '11 класс'),

    ('1 курс ', '1 курс'),
    ('2 курс', '2 курс'),
    ('3 курс', '3 курс'),
    ('4 курс', '4 курс'),

]


class MemberModel(models.Model):
    first_name = models.CharField()
    second_name = models.CharField()
    last_name = models.CharField()

    status = models.CharField(choices=MEMBER_STATUS_CHOICES, blank=False, null=False)

    team = models.ForeignKey(TeamModel, on_delete=models.PROTECT, blank=True, null=True)

    email = models.EmailField()
    phone = models.CharField()
    tg_username = models.CharField()

    date_of_birth = models.DateField(blank=False, null=True)
    city = models.CharField()
    school = models.CharField()
    grade = models.CharField(choices=MEMBER_GRADE_CHOICES, blank=True, null=True, default=None)
    subjects = models.CharField(blank=False, null=True)
    languages = models.TextField(blank=False, null=True, default="Русский - родной")

    skills = models.TextField(blank=False, null=True)
    hobbies = models.TextField(blank=False, null=True)
    achievements = models.TextField(blank=False, null=True)

    more_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.second_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.second_name} {self.last_name}"

    def get_username(self):
        return self.tg_username.replace('@', '')

    def get_all_info(self):
        return {
            'статус': self.status,
            'совет': self.team,
            'email': self.email,
            'телефон': self.phone,
            'дата рождения': self.date_of_birth,
            'город проживания': self.city,
            'образование': self.school,
            'класс/курс': self.grade if self.grade else "-",
            'учебная сфера интересов': self.subjects,
            'Иностранные языки': self.languages,
            'навыки': self.skills,
            'увлечения': self.hobbies,
            'достижения': self.achievements,
            'доп. информация': self.more_info,
        }

    @staticmethod
    def get_team_members(team_name):
        return MemberModel.objects.filter(team__name=team_name)

    @staticmethod
    def get_team_member_num(team_name):
        return MemberModel.objects.filter(team__name=team_name).count()
