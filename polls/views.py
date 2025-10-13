from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db import IntegrityError
from django.forms import formset_factory
from .models import Poll, Choice, Vote
from .forms import RegisterForm, PollForm, ChoiceForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('polls:poll_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('polls:poll_list')
    else:
        form = RegisterForm()
    return render(request, 'polls/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('polls:poll_list')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('polls:poll_list')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'polls/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('polls:login')

@login_required
def poll_list(request):
    polls = Poll.objects.filter(is_active=True).order_by('-created_at')
    user_votes = Vote.objects.filter(user=request.user).values_list('choice__poll_id', flat=True)
    return render(request, 'polls/poll_list.html', {'polls': polls, 'user_votes': list(user_votes)})

@login_required
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, is_active=True)
    has_voted = Vote.objects.filter(user=request.user, choice__poll=poll).exists()
    if request.method == 'POST' and not has_voted:
        choice_id = request.POST.get('choice')
        if choice_id:
            choice = get_object_or_404(Choice, id=choice_id, poll=poll)
            try:
                Vote.objects.create(user=request.user, choice=choice)
                messages.success(request, 'Vote recorded!')
                return redirect('polls:results', poll_id=poll.id)
            except:
                messages.error(request, 'Already voted')
    return render(request, 'polls/poll_detail.html', {'poll': poll, 'has_voted': has_voted})

@login_required
def results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, 'polls/results.html', {'poll': poll})

@staff_member_required
def create_poll(request):
    ChoiceFormSet = formset_factory(ChoiceForm, extra=4, min_num=2, validate_min=True)
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST)
        if poll_form.is_valid() and choice_formset.is_valid():
            poll = poll_form.save(commit=False)
            poll.created_by = request.user
            poll.save()
            for choice_form in choice_formset:
                if choice_form.cleaned_data.get('choice_text'):
                    choice = choice_form.save(commit=False)
                    choice.poll = poll
                    choice.save()
            messages.success(request, f'Poll created!')
            return redirect('polls:manage_polls')
    else:
        poll_form = PollForm()
        choice_formset = ChoiceFormSet()
    return render(request, 'polls/create_poll.html', {'poll_form': poll_form, 'choice_formset': choice_formset})

@staff_member_required
def manage_polls(request):
    polls = Poll.objects.all().order_by('-created_at')
    return render(request, 'polls/manage_polls.html', {'polls': polls})

@staff_member_required
def edit_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == 'POST':
        poll_form = PollForm(request.POST, instance=poll)
        if poll_form.is_valid():
            poll_form.save()
            messages.success(request, 'Poll updated!')
            return redirect('polls:manage_polls')
    else:
        poll_form = PollForm(instance=poll)
    return render(request, 'polls/edit_poll.html', {'poll': poll, 'poll_form': poll_form})

@staff_member_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == 'POST':
        poll.delete()
        messages.success(request, 'Poll deleted!')
        return redirect('polls:manage_polls')
    return render(request, 'polls/delete_poll.html', {'poll': poll})

@staff_member_required
def toggle_poll_status(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    poll.is_active = not poll.is_active
    poll.save()
    messages.success(request, f'Poll {"activated" if poll.is_active else "deactivated"}!')
    return redirect('polls:manage_polls')