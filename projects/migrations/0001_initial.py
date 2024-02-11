# Generated by Django 5.0 on 2024-01-12 16:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="GrantModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="ProjectModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(unique=True)),
                ("description", models.CharField()),
                ("manager", models.CharField(blank=True, null=True)),
                ("author", models.CharField(blank=True, null=True)),
                (
                    "period_type",
                    models.CharField(
                        choices=[
                            ("долгосрочный", "долгосрочный"),
                            ("краткосрочный", "краткосрочный"),
                        ],
                        max_length=20,
                    ),
                ),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("status", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="TeamModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField()),
                ("vk_link", models.URLField(blank=True, null=True)),
                ("person_from_gov", models.CharField(blank=True, null=True)),
                ("person_from_company", models.CharField(blank=True, null=True)),
                ("found_date", models.DateField(blank=True, null=True)),
                ("manager", models.CharField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="SponsoredMoneyModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("money", models.FloatField()),
                (
                    "grant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="projects.grantmodel",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="projects.projectmodel",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="projectmodel",
            name="by_team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="projects.teammodel"
            ),
        ),
        migrations.CreateModel(
            name="MemberModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField()),
                ("second_name", models.CharField()),
                ("last_name", models.CharField()),
                (
                    "status",
                    models.CharField(
                        choices=[("школьник", "школьник"), ("студент", "студент")]
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField()),
                ("tg_username", models.CharField()),
                ("date_of_birth", models.DateField(null=True)),
                ("city", models.CharField()),
                ("school", models.CharField()),
                ("subjects", models.CharField(null=True)),
                ("skills", models.TextField(null=True)),
                ("hobbies", models.TextField(null=True)),
                ("achievements", models.TextField(null=True)),
                ("more_info", models.TextField(blank=True, null=True)),
                (
                    "team",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="projects.teammodel",
                    ),
                ),
            ],
        ),
    ]
