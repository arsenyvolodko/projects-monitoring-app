from django.db.models import ProtectedError
from django.shortcuts import render, get_object_or_404, redirect

from projects.models import TeamModel
from teams.forms import NewTeamForm


def all_teams(request):
    junior_teams = TeamModel.objects.all()
    return render(request, 'teams/all_teams.html', {'teams': junior_teams})


def specific_team(request, team_id):
    team = get_object_or_404(TeamModel, pk=team_id)
    return render(request, 'teams/specific_team.html', {'team': team})


def add_new_team(request):
    if request.method == 'GET':
        return render(request, 'teams/add_new_team.html', {'form': NewTeamForm})
    else:
        try:
            form = NewTeamForm(request.POST)
            new_project = form.save(commit=False)
            new_project.save()
            return redirect('team:all_teams')
        except ValueError:
            return render(request, 'teams/add_new_team.html',
                          {'form': NewTeamForm(), 'error': 'Что-то заполнено не так'})
        except IndentationError:
            return render(request, 'teams/add_new_team.html',
                          {'form': NewTeamForm(), 'error': 'Проект с таким названием уже существует'})


def edit_team(request, team_id):
    team = get_object_or_404(TeamModel, pk=team_id)
    if request.method == 'POST':
        form = NewTeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('team:specific_team', team_id=team_id)
    else:
        form = NewTeamForm(instance=team)

    return render(request, 'teams/edit_team.html', {'form': form, 'team': team, })


def delete_team(request, team_id):
    team = get_object_or_404(TeamModel, pk=team_id)
    teams = TeamModel.objects.all()
    try:
        if request.method == 'POST':
            team.delete()
            return redirect('team:all_teams')
        else:
            return render(request, 'teams/all_teams.html', {'teams': teams})
    except Exception:
        return render(request, 'teams/specific_team.html', {'team': team, 'error': 'Ошибка при удалении команды. Скорее всего, это связно с тем, что есть проекты, которые ею реализуются, а также участники, которые в ней состоят. Чтобы удалить команду необходимо, необходимо удалить все проекты, которые ею реализуются, а также всех участников, которые в ней состоят.'})