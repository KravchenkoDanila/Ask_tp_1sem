from django.http import HttpResponse
from django.shortcuts import render
from . import models

base_context = {'questions': models.questions, 'tags': models.tags}

# Create your views here.
def index(request):
    context = {'answers': len(models.questions)}
    context.update(base_context)
    return render(request, 'index.html', context)


def hot(request):
    context = {'questions': models.questions }
    return render(request, 'index.html', context)


def tag(request, tag_name):
    for i in models.questions:
        if i['tag_name'] == tag_name:
            context = {'question': models.questions[i['id'] - 1]}
            context.update(base_context)
            return render(request, 'tag.html', context)
    # context = {'questions': models.questions, 'tag': tag_name}
    # return render(request, 'tag.html', context)


def question(request, question_id):
    context = {'question': models.questions[question_id - 1]}
    context.update(base_context)
    return render(request, 'question.html', context)


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'register.html')


def ask(request):
    return render(request, 'ask.html')

