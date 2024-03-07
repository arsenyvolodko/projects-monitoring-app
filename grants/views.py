from django.db.models import ProtectedError
from django.shortcuts import render, redirect

from grants.forms import NewGrantForm, NewSponsoredMoneyForm
from projects.models import SponsoredMoneyModel, ProjectModel, GrantModel
from projects.views import edit_sponsored_money, delete_sponsored_money


def all_grants(request):
    grants = GrantModel.objects.all()
    sponsored_money = SponsoredMoneyModel.objects.all()
    projects = ProjectModel.objects.all()
    return render(request, 'grants/all_grants.html', {'grants': grants, 'projects': projects,
                                                      'sponsored_money': sponsored_money})


def add_new_grant(request):
    if request.method == 'GET':
        return render(request, 'grants/add_new_grant.html', {'form': NewGrantForm})
    else:
        try:
            form = NewGrantForm(request.POST)  # создаем форму
            new_grant = form.save(commit=False)
            new_grant.save()
            return redirect('grant:all_grants')
        except ValueError:
            return render(request, 'grants/add_new_grant.html',
                          {'form': NewGrantForm(), 'error': 'Что-то заполнено не так'})
        except IndentationError:
            return render(request, 'grants/add_new_grant.html',
                          {'form': NewGrantForm(), 'error': 'Проект с таким названием уже существует'})


def specific_grant(request, grant_id):
    grant = GrantModel.objects.get(pk=grant_id)
    return render(request, 'grants/specific_grant.html', {'grant': grant, })


def add_sponsored_money(request, grant_id):
    if request.method == 'GET':
        return render(request, 'grants/add_sponsored_money.html', {'form': NewSponsoredMoneyForm})
    else:
        try:
            form = NewSponsoredMoneyForm(request.POST)  # создаем форму
            new_sponsored_money = form.save(commit=False)
            new_sponsored_money.grant = GrantModel.objects.get(pk=grant_id)
            new_sponsored_money.save()
            return redirect('grant:specific_grant', grant_id=grant_id)
        except ValueError:
            return render(request, 'grants/add_sponsored_money.html',
                          {'form': NewSponsoredMoneyForm(), 'error': 'Что-то заполнено не так'})
        except IndentationError:
            return render(request, 'grants/add_sponsored_money.html',
                          {'form': NewSponsoredMoneyForm(), 'error': 'Проект с таким названием уже существует'})


def edit_sponsored_money_in_grants(request, project_id, grant_id):
    to_page = f'grant:specific_grant'
    return edit_sponsored_money(request, project_id, grant_id, to_page)


def delete_sponsored_money_in_grants(request, project_id, grant_id):
    grant = GrantModel.objects.get(pk=grant_id)
    models = SponsoredMoneyModel.get_model_by_project_and_grant(project_id, grant_id)
    if not models:
        raise AssertionError("BEDA")
    sponsored_money = models[0]
    try:
        if request.method == 'POST':
            sponsored_money.delete()
            return redirect('grant:specific_grant', grant_id=grant_id)
        else:
            return render(request, 'grants/specific_grant.html', {'grant': grant})
    except Exception:
        return render(request, 'grants/specific_grant.html', {'grant': grant,
                                                              'error': 'почему-то не удаляется :(\n''айтишник посредственный оказался'})


def edit_grant(request, grant_id):
    grant = GrantModel.objects.get(pk=grant_id)
    if request.method == 'POST':
        form = NewGrantForm(request.POST, instance=grant)
        if form.is_valid():
            form.save()
            return redirect('grant:specific_grant', grant_id=grant_id)
    else:
        form = NewGrantForm(instance=grant)

    return render(request, 'grants/edit_grant.html', {'form': form, 'grant': grant, })


def delete_grant(request, grant_id):
    grant = GrantModel.objects.get(pk=grant_id)
    grants = GrantModel.objects.all()
    try:
        if request.method == 'POST':
            grant.delete()
            return redirect('grant:all_grants')
        else:
            return render(request, 'grants/all_grants.html', {'grants': grants})
    except ProtectedError:
        return render(request, 'grants/specific_grant.html',
                      {'grant': grant, 'error': 'Не удается удалить грант. Скорее всего это связано с тем, что есть проекты, связанные с этим грантом. Для того чтобы удалить грант, необходимо удалить все проекты, связанные с ним.'})
    except Exception:
        return render(request, 'grants/specific_grant.html',
                      {'grant': grant, 'error': 'почему-то не удаляется :(\n''айтишник посредственный оказался'})