from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewProjectForm, NewSponsoredMoneyForm
from django.db.models.deletion import ProtectedError
from .models import ProjectModel, SponsoredMoneyModel


def all_projects(request):
    projects = ProjectModel.objects.all()
    return render(request, 'projects/all_projects.html', {'projects': projects})


def edit_project(request, project_id):
    project = get_object_or_404(ProjectModel, pk=project_id)
    if request.method == 'POST':
        form = NewProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project:specific_project', project_id=project_id)
    else:
        form = NewProjectForm(instance=project)

    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})


def specific_project(request, project_id):
    project = get_object_or_404(ProjectModel, pk=project_id)
    return render(request, 'projects/specific_project.html', {'project': project})


def add_new_project(request):
    if request.method == 'GET':
        return render(request, 'projects/add_new_project.html', {'form': NewProjectForm})
    else:
        try:
            form = NewProjectForm(request.POST)
            new_project = form.save(commit=False)
            new_project.save()
            return redirect('project:all_projects')
        except ValueError:
            return render(request, 'projects/add_new_project.html',
                          {'form': NewProjectForm(), 'error': 'Что-то заполнено не так'})
        except IndentationError:
            return render(request, 'projects/add_new_project.html',
                          {'form': NewProjectForm(), 'error': 'Проект с таким названием уже существует'})


def delete_project(request, project_id):
    project = get_object_or_404(ProjectModel, pk=project_id)
    projects = ProjectModel.objects.all()
    try:
        if request.method == 'POST':
            project.delete()
            return redirect('project:all_projects')
        else:
            return render(request, 'projects/all_projects.html', {'projects': projects})
    except ProtectedError as e:
        return render(request, 'projects/specific_project.html',
                      {'project': project,
                       'error': 'Нельзя удалить проект до тех пор, пока существуют гранты, в которых проект участвовал.\n'
                                'Для удаления проекта необходимо удалить записи о полученных средствах в рамках грантов, в которых участвовал проект.\n'
                                'Для этого необходимо перейти на страницу грантов, открыть страницу конкретного гранта, в котором участвовал проект,'
                                ' и удалить записи о полученных средствах (там справа напротив каждого участвовавшего проекта есть кнопочка корзины).'})
    except Exception as e:
        print(e, type(e))
        return render(request, 'projects/specific_project.html', {'project': project,
                                                                  'error': 'почему-то не удаляется :(\n''айтишник посредственный оказался'})


def add_sponsored_money(request, project_id):
    projects = ProjectModel.objects.all()
    if request.method == 'GET':
        return render(request, 'projects/add_sponsored_money.html', {'form': NewSponsoredMoneyForm})
    else:
        form = NewSponsoredMoneyForm(request.POST)
        try:
            new_project = form.save(commit=False)
            new_project.project = ProjectModel.objects.get(pk=project_id)
            new_project.save()
            return redirect('project:specific_project', project_id=project_id)
        except ValueError:
            return render(request, 'projects/all_projects.html',
                          {'projects': projects, 'error': form.errors})
        except IndentationError:
            return render(request, 'projects/all_projects.html',
                          {'projects': projects, 'error': form.errors})


def edit_sponsored_money(request, project_id, grant_id, to_page='project:specific_project'):
    models = SponsoredMoneyModel.get_model_by_project_and_grant(project_id, grant_id)
    if not models:
        raise AssertionError("BEDA")
    sponsored_money = models[0]
    if request.method == 'POST':
        form = NewSponsoredMoneyForm(request.POST, instance=sponsored_money)
        if form.is_valid():
            form.save()
            if 'project' in to_page:
                return redirect(to_page, project_id=project_id)
            else:
                return redirect(to_page, grant_id=grant_id)
    else:
        form = NewSponsoredMoneyForm(instance=sponsored_money)

    return render(request, 'projects/edit_sponsored_money.html', {'form': form, 'sponsored_money': sponsored_money})


def delete_sponsored_money(request, project_id, grant_id, to_page='project:specific_project'):
    models = SponsoredMoneyModel.get_model_by_project_and_grant(project_id, grant_id)
    if not models:
        raise AssertionError("BEDA")
    sponsored_money = models[0]
    try:
        if request.method == 'POST':
            sponsored_money.delete()
            if 'project' in to_page:
                return redirect(to_page, project_id=project_id)
            else:
                return redirect(to_page, grant_id=grant_id)
        else:
            return render(request, 'projects/specific_project.html', {'sponsored_money': sponsored_money})
    except Exception:
        return render(request, 'projects/specific_project.html', {'sponsored_money': sponsored_money,
                                                                  'error': 'почему-то не удаляется :(\n''айтишник посредственный оказался'})
