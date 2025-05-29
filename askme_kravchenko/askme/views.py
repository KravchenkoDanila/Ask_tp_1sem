from django.contrib import auth
from django.db.models import Sum
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .models import Question, Tag, Answer, Profile
from .utils import paginate
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm, SettingsForm, AddQuestionForm, AddAnswerForm


def index(request):
    questions = Question.objects.new()
    paginated_data = paginate(questions, request)

    context = {
        'page_obj': paginated_data['page_obj'],
        'paginator': paginated_data['paginator'],
        'is_paginated': paginated_data['is_paginated'],
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.top()
    }

    return render(request, 'index.html', context)


# def question(request, question_id):
#     question = get_object_or_404(Question.objects.with_like_sum(), pk=question_id)
#     answers = Answer.objects.for_question(question_id)
#     paginated_answers = paginate(answers, request)
#
#     context = {
#         'question': question,
#         'page_obj': paginated_answers['page_obj'],
#         'paginator': paginated_answers['paginator'],
#         'is_paginated': paginated_answers['is_paginated'],
#         'tags': Tag.objects.popular(),
#     }
#
#     return render(request, 'question.html', context)


def question(request, question_id):
    question = get_object_or_404(Question.objects.with_like_sum(), pk=question_id)
    answers = Answer.objects.for_question(question_id)
    paginated_answers = paginate(answers, request)

    if request.user.is_authenticated:
        form = AddAnswerForm(request.POST or None)
        if form.is_valid():
            form.save(author=request.user.profile, question=question)
            return redirect('question', question_id=question_id)
    else:
        return redirect('Login')

    context = {
        'question': question,
        'page_obj': paginated_answers['page_obj'],
        'paginator': paginated_answers['paginator'],
        'is_paginated': paginated_answers['is_paginated'],
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.top(),
        'form': form
    }

    return render(request, 'question.html', context)


def hot(request):
    questions = Question.objects.best()
    paginated_data = paginate(questions, request)

    context = {
        'page_obj': paginated_data['page_obj'],
        'paginator': paginated_data['paginator'],
        'is_paginated': paginated_data['is_paginated'],
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.top()
    }

    return render(request, 'hot.html', context)


def tag(request, tag_name):
    try:
        questions = Question.objects.filter(tags__name=tag_name).annotate(
            like_sum=Sum('question_likes__value')
        ).distinct()
    except Exception as e:
        raise Http404("Тег не существует")

    if not questions.exists():
        raise Http404(f"Нет вопросов по тегу {tag_name}")

    paginated_data = paginate(questions, request)

    context = {
        'page_obj': paginated_data['page_obj'],
        'paginator': paginated_data['paginator'],
        'is_paginated': paginated_data['is_paginated'],
        'page_title': tag_name,
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.top()
    }

    return render(request, 'tag.html', context)


def log_in(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            auth.login(request, user)
            return redirect('/')

    context = {
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.top(),
        'form': form
    }
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('/')


def signup(request):
    form = SignupForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user = form.save(commit=True)
        auth.login(request, user)
        return redirect('/')
    context = {
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.top(),
        'form': form
    }
    return render(request, 'register.html', context)



@login_required
def settings(request):
    profile = request.user.profile  # <-- Получаем существующий профиль

    form = SettingsForm(
        request.POST or None,
        request.FILES or None,
        instance=profile,  # <-- Передаем instance, чтобы редактировать, а не создавать
        user=request.user
    )

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('settings')
    context = {
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.top(),
        'form': form
    }

    return render(request, 'settings.html', context)


@login_required
def ask(request):
    form = AddQuestionForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        question = form.save(commit=True, author=request.user.profile)
        return redirect('question', question_id=question.id)
    context = {
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.top(),
        'form': form
    }
    return render(request, 'ask.html', context)


# def login(request):
#     return render(request, 'login.html', {'tags': Tag.objects.popular()})
#
#
# def signup(request):
#     return render(request, 'register.html', {'tags': Tag.objects.popular()})


# def settings(request):
#     return render(request, 'settings.html', {'tags': Tag.objects.popular()})


# def ask(request):
#     return render(request, 'ask.html', {'tags': Tag.objects.popular()})