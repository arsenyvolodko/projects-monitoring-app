from django.shortcuts import render, get_object_or_404, redirect

from members.forms import NewMemberForm
from projects.models import MemberModel, TeamModel


# def all_teams(request):
#     junior_teams = TeamModel.objects.all()
#     return render(request, 'teams/all_teams.html', {'teams': junior_teams})


def all_members(request):
    members = MemberModel.objects.all()
    teams = TeamModel.objects.all()
    return render(request, 'members/all_members.html', {'members': members, 'teams': teams})


# def specific_team(request, team_id):
#     team = get_object_or_404(TeamModel, pk=team_id)
#     return render(request, 'teams/specific_team.html', {'team': team})

def specific_member(request, member_id):
    member = get_object_or_404(MemberModel, pk=member_id)
    return render(request, 'members/specific_member.html', {'member': member})


def add_new_member(request):
    if request.method == 'GET':
        return render(request, 'members/add_new_member.html', {'form': NewMemberForm})
    else:
        form = NewMemberForm(request.POST)
        if form.is_valid():
            new_member = form.save(commit=False)
            new_member.save()
            return redirect('members:all_members')
        else:
            return render(request, 'members/add_new_member.html',
                          {'form': NewMemberForm(), 'error': form.errors})


def edit_member(request, member_id):
    member = get_object_or_404(MemberModel, pk=member_id)
    if request.method == 'POST':
        form = NewMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('members:specific_member', member_id=member_id)
    else:
        form = NewMemberForm(instance=member)

    return render(request, 'members/edit_member.html', {'form': form, 'member': member})


def delete_member(request, member_id):
    member = get_object_or_404(MemberModel, pk=member_id)
    members = MemberModel.objects.all()
    try:
        if request.method == 'POST':
            member.delete()
            return redirect('members:all_members')
    except Exception as e:
        return render(request, 'members/specific_member.html', {'member': member,
                                                                'error': 'почему-то не удаляется :(\n''айтишник посредственный оказался'})
    return render(request, 'members/all_members.html', {'members': members})
