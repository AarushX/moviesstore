from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import PetitionForm
from .models import Petition, PetitionVote

def petition_list(request):
    petitions = Petition.objects.all()
    template_data = {'title': 'Petitions'}
    return render(request, 'petitions/index.html', {
        'petitions': petitions,
        'template_data': template_data,
    })


@login_required
def petition_create(request):
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, 'Petition created.')
            return redirect('petitions:detail', pk=petition.pk)
    else:
        form = PetitionForm()
    template_data = {'title': 'Create Petition'}
    return render(request, 'petitions/create.html', {'form': form, 'template_data': template_data})


def petition_detail(request, pk: int):
    petition = get_object_or_404(Petition, pk=pk)
    has_voted = False
    if request.user.is_authenticated:
        has_voted = PetitionVote.objects.filter(petition=petition, user=request.user).exists()
    template_data = {'title': petition.title}
    return render(request, 'petitions/detail.html', {
        'petition': petition,
        'has_voted': has_voted,
        'template_data': template_data,
    })


@login_required
def petition_vote_yes(request, pk: int):
    petition = get_object_or_404(Petition, pk=pk)
    if request.method != 'POST':
        return redirect('petitions:detail', pk=petition.pk)
    _, created = PetitionVote.objects.get_or_create(petition=petition, user=request.user, defaults={'value': True})
    if created:
        messages.success(request, 'Thanks for voting!')
    else:
        messages.info(request, 'You already voted on this petition.')
    return redirect('petitions:detail', pk=petition.pk)
