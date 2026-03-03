from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db import IntegrityError
from django.forms import formset_factory, modelformset_factory
from django import forms as django_forms
from django.contrib.auth.models import User
from .models import Poll, Choice, Vote, Community
from .forms import RegisterForm, PollForm, ChoiceForm, CommunityForm

# ==================== COMMUNITY VIEWS ====================

@login_required
def dashboard(request):
    managed_communities = request.user.administered_communities.all()
    your_communities = request.user.joined_communities.all()
    discover_communities = Community.objects.exclude(id__in=managed_communities).exclude(id__in=your_communities)
    
    return render(request, 'polls/dashboard.html', {
        'managed_communities': managed_communities,
        'your_communities': your_communities,
        'discover_communities': discover_communities
    })

@login_required
def create_community(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.admin = request.user
            community.save()
            community.members.add(request.user)
            messages.success(request, f'Community "{community.name}" created successfully!')
            return redirect('polls:dashboard')
    else:
        form = CommunityForm()
    return render(request, 'polls/create_community.html', {'form': form})

@login_required
def join_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.method == 'POST':
        if request.user not in community.members.all():
            community.members.add(request.user)
            messages.success(request, f'You have joined {community.name}!')
    return redirect('polls:dashboard')

@login_required
def leave_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.method == 'POST':
        if request.user in community.members.all() and request.user != community.admin:
            community.members.remove(request.user)
            messages.success(request, f'You have left {community.name}.')
            return redirect('polls:dashboard')
    
    return render(request, 'polls/leave_community.html', {'community': community})

@login_required
def manage_community(request, community_id):
    community = get_object_or_404(Community, id=community_id, admin=request.user)
    
    if request.method == 'POST':
        form = CommunityForm(request.POST, instance=community)
        if form.is_valid():
            form.save()
            messages.success(request, 'Community details updated successfully!')
            return redirect('polls:manage_community', community_id=community.id)
    else:
        form = CommunityForm(instance=community)
        
    members = community.members.exclude(id=request.user.id)
    return render(request, 'polls/manage_community.html', {
        'community': community,
        'form': form,
        'members': members
    })

@login_required
def remove_member(request, community_id, user_id):
    community = get_object_or_404(Community, id=community_id, admin=request.user)
    user_to_remove = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST' and user_to_remove != community.admin:
        community.members.remove(user_to_remove)
        messages.success(request, f'{user_to_remove.username} removed from the community.')
        return redirect('polls:manage_community', community_id=community.id)
        
    return render(request, 'polls/remove_member.html', {
        'community': community,
        'user_to_remove': user_to_remove
    })

@login_required
def delete_community(request, community_id):
    community = get_object_or_404(Community, id=community_id, admin=request.user)
    if request.method == 'POST':
        name = community.name
        community.delete()
        messages.success(request, f'Community "{name}" was successfully deleted.')
        return redirect('polls:dashboard')
    return render(request, 'polls/delete_community.html', {'community': community})

# ==================== USER VIEWS ====================

def register_view(request):
    if request.user.is_authenticated:
        return redirect('polls:dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to PollNest.')
            return redirect('polls:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'polls/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('polls:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('polls:dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'polls/login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out successfully.')
        return redirect('polls:login')
    
    return render(request, 'polls/logout_confirm.html')

@login_required
def poll_list(request):
    community_id = request.GET.get('community')
    current_community = None
    
    if community_id:
        current_community = get_object_or_404(Community, id=community_id)
        if request.user not in current_community.members.all():
            messages.error(request, 'You must be a member to view these polls.')
            return redirect('polls:dashboard')
        polls = Poll.objects.filter(is_active=True, community=current_community).order_by('-created_at')
    else:
        polls = Poll.objects.filter(is_active=True, community__isnull=True).order_by('-created_at')
        
    user_votes = Vote.objects.filter(user=request.user).values_list('choice__poll_id', flat=True)
    return render(request, 'polls/poll_list.html', {
        'polls': polls,
        'user_votes': list(user_votes),
        'current_community': current_community
    })

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
                messages.success(request, '✓ Your vote has been recorded successfully!')
                return redirect('polls:results', poll_id=poll.id)
            except IntegrityError:
                messages.error(request, 'You have already voted on this poll.')
    
    return render(request, 'polls/poll_detail.html', {
        'poll': poll,
        'has_voted': has_voted
    })

@login_required
def results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, 'polls/results.html', {'poll': poll})

# ==================== ADMIN VIEWS ====================

@staff_member_required
def create_poll(request):
    community_id = request.GET.get('community')
    
    if not community_id:
        messages.error(request, 'Please select a community to create a poll in.')
        return redirect('polls:dashboard')
        
    community = get_object_or_404(Community, id=community_id, admin=request.user)

    ChoiceFormSet = formset_factory(ChoiceForm, extra=4, min_num=2, validate_min=True)
    
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST)
        
        if poll_form.is_valid() and choice_formset.is_valid():
            poll = poll_form.save(commit=False)
            poll.created_by = request.user
            poll.community = community
            poll.save()
            
            for choice_form in choice_formset:
                if choice_form.cleaned_data.get('choice_text'):
                    choice = choice_form.save(commit=False)
                    choice.poll = poll
                    choice.save()
            
            messages.success(request, f'Poll "{poll.question}" created successfully!')
            return redirect(f"{reverse('polls:manage_polls')}?community={poll.community.id}")
    else:
        poll_form = PollForm()
        choice_formset = ChoiceFormSet()
    
    return render(request, 'polls/create_poll.html', {
        'poll_form': poll_form,
        'choice_formset': choice_formset,
        'current_community': community
    })

@login_required
def manage_polls(request):
    community_id = request.GET.get('community')
    
    if not community_id:
        messages.error(request, 'Please select a community to manage its polls.')
        return redirect('polls:dashboard')
        
    current_community = get_object_or_404(Community, id=community_id, admin=request.user)
    polls = Poll.objects.filter(community=current_community).order_by('-created_at')
        
    return render(request, 'polls/manage_polls.html', {
        'polls': polls,
        'current_community': current_community
    })

@staff_member_required
def edit_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    
    # Create a formset for existing choices
    ChoiceFormSet = modelformset_factory(
        Choice, 
        fields=('choice_text',), 
        extra=2,  # Allow adding 2 new choices
        can_delete=True,
        widgets={'choice_text': django_forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter choice text...'})}
    )
    
    if request.method == 'POST':
        poll_form = PollForm(request.POST, instance=poll)
        choice_formset = ChoiceFormSet(request.POST, queryset=Choice.objects.filter(poll=poll))
        
        if poll_form.is_valid() and choice_formset.is_valid():
            poll_form.save()
            
            # Save choices
            choices = choice_formset.save(commit=False)
            for choice in choices:
                if choice.choice_text and choice.choice_text.strip():
                    choice.choice_text = choice.choice_text.strip()
                    choice.poll = poll
                    choice.save()
            
            # Delete marked choices
            for choice in choice_formset.deleted_objects:
                choice.delete()
            
            messages.success(request, f'Poll "{poll.question}" updated successfully!')
            if poll.community:
                return redirect(f"{reverse('polls:manage_polls')}?community={poll.community.id}")
            return redirect('polls:manage_polls')
    else:
        poll_form = PollForm(instance=poll)
        choice_formset = ChoiceFormSet(queryset=Choice.objects.filter(poll=poll))
    
    return render(request, 'polls/edit_poll.html', {
        'poll': poll,
        'poll_form': poll_form,
        'choice_formset': choice_formset
    })


@staff_member_required
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    
    if request.method == 'POST':
        choice_text = request.POST.get('choice_text')
        if choice_text:
            Choice.objects.create(poll=poll, choice_text=choice_text)
            messages.success(request, 'Choice added successfully!')
        else:
            messages.error(request, 'Choice text cannot be empty!')
    
    return redirect('polls:edit_poll', poll_id=poll.id)


@staff_member_required
def delete_choice(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    poll_id = choice.poll.id
    
    # Check if poll has at least 3 choices (so we can delete one)
    if choice.poll.choices.count() <= 2:
        messages.error(request, 'Cannot delete! Poll must have at least 2 choices.')
    else:
        choice.delete()
        messages.success(request, 'Choice deleted successfully!')
    
    return redirect('polls:edit_poll', poll_id=poll_id)

@staff_member_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    
    if request.method == 'POST':
        question = poll.question
        poll.delete()
        messages.success(request, f'Poll "{question}" deleted successfully!')
        if poll.community:
            return redirect(f"{reverse('polls:manage_polls')}?community={poll.community.id}")
        return redirect('polls:manage_polls')
    
    return render(request, 'polls/delete_poll.html', {'poll': poll})

@staff_member_required
def toggle_poll_status(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    poll.is_active = not poll.is_active
    poll.save()
    
    status = "activated" if poll.is_active else "deactivated"
    messages.success(request, f'Poll "{poll.question}" {status}!')
    if poll.community:
        return redirect(f"{reverse('polls:manage_polls')}?community={poll.community.id}")
    return redirect('polls:manage_polls')