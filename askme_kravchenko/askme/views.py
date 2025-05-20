from django.http import HttpResponse
from django.shortcuts import render
from . import models
from .utils import paginate


def index(request):

    paginated_data = paginate(models.questions, request)

    context = {
        'page_obj': paginated_data['page_obj'],
        'paginator': paginated_data['paginator'],
        'is_paginated': paginated_data['is_paginated'],
        'tags': models.tags,
    }
    # print(paginated_data['is_paginated'])
    return render(request, 'index.html', context)


def question(request, question_id):

    paginated_answers = paginate(models.answers, request)

    context = {
        'question': models.questions[question_id - 1],
        'page_obj': paginated_answers['page_obj'],
        'paginator': paginated_answers['paginator'],
        'is_paginated': paginated_answers['is_paginated'],
        'tags': models.tags,
    }

    return render(request, 'question.html', context)


def hot(request):
    questions_page = paginate(models.questions, request)

    context = {
        'questions': questions_page,
        'tags': models.tags,
    }
    return render(request, 'hot.html', context)


def tag(request, tag_name):
    tag_questions = []
    for i in models.questions:
        if i['tag_name'] == tag_name:
            tag_questions.append(i)

    paginated_answers = paginate(tag_questions, request)

    context = {
        'page_obj': paginated_answers['page_obj'],
        'paginator': paginated_answers['paginator'],
        'is_paginated': paginated_answers['is_paginated'],
        'page_title': tag_name,
        'tags': models.tags
    }
    return render(request, 'tag.html', context)
        # return 404


def login(request):
    context = {'tags': models.tags}
    return render(request, 'login.html', context)


def signup(request):
    context = {'tags': models.tags}
    return render(request, 'register.html', context)


def settings(request):
    context = {'tags': models.tags}
    return render(request, 'settings.html', context)


def ask(request):
    context = {'tags': models.tags}
    return render(request, 'ask.html', context)



# def index(request):
#
#     questions_page = paginate(models.questions, request)
#
#     context = {
#         'questions': models.questions,
#         'tags': models.tags,
#     }
#
#     return render(request, 'index.html', context)

#
# def question(request, question_id):
#
#     answers_page = paginate(models.ansvers, request)
#
#     context = {'question': models.questions[question_id - 1], 'tags': models.tags, 'answers': answers_page}
#
#     return render(request, 'question.html', context)