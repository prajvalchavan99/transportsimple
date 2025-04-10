from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.db.models import Count
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from forum import models as ForumModels

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authentication:login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    next_url = request.GET.get('next')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect(request.POST.get('next') or 'authentication:dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {
        'form': form,
        'next': next_url
    })

def logout_view(request):
    logout(request)
    return redirect('authentication:login')

def dashboard_view(request):
    context = {}
    questions_to_answer = ForumModels.Question.objects.annotate(answer_count=Count('answers')) \
        .order_by('answer_count', '-created_at')[:5]
    context['questions_to_answer'] = questions_to_answer
    if request.user.is_authenticated:
        context['question_list'] = ForumModels.Question.objects.filter(user=request.user) \
            .annotate(answer_count=Count('answers'))
        questions_to_answer = ForumModels.Question.objects.exclude(user=request.user) \
            .annotate(answer_count=Count('answers')) \
            .order_by('answer_count', '-created_at')[:5]
        context['questions_to_answer'] = questions_to_answer
    return render(request, 'dashboard.html', context)